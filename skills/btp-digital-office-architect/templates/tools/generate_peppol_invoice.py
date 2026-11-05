"""
Script to generate standard Peppol BIS Billing 3.0 UBL 2.1 XML electronic invoices.
Complies with the mandatory Belgian B2B electronic invoicing legislation (applicable Jan 1, 2026).
Converts accepted quotes into compliant Peppol XML files.
Strictly typed, zero 'Any'.
"""

import argparse
import os
import sys
from datetime import date, timedelta
from typing import Final, List, Optional, Tuple, TypedDict
import xml.etree.ElementTree as ET

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


class PeppolInvoiceData(TypedDict):
    invoice_number: str
    issue_date: date
    due_date: date
    supplier_name: str
    supplier_cbe: str  # Numéro d'entreprise belge BCE / KBO (ex: 0459180573)
    supplier_vat: str  # BE0459180573
    supplier_street: str
    supplier_city: str
    supplier_postal_code: str
    customer_name: str
    customer_cbe: str
    customer_vat: str
    customer_street: str
    customer_city: str
    customer_postal_code: str
    item_description: str
    amount_htva: float
    vat_rate: float  # Ex: 0.21


def create_peppol_ubl_xml(data: PeppolInvoiceData) -> str:
    """
    Construit une chaîne XML UBL 2.1 conforme au profil Peppol BIS Billing 3.0 (EN 16931).

    Paramètres :
        data (PeppolInvoiceData) : Données d'en-tête, parties prenantes et montants.

    Retour :
        str : Document XML UBL complet indenté.
    """
    vat_amount = round(data["amount_htva"] * data["vat_rate"], 2)
    total_ttc = round(data["amount_htva"] + vat_amount, 2)
    rate_percent = int(data["vat_rate"] * 100)

    # Racine UBL Invoice
    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
         xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
         xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2">
    <!-- Identifiants Peppol BIS Billing 3.0 obligatoires -->
    <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:fdc:peppol.eu:2017:poacc:billing:3.0</cbc:CustomizationID>
    <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
    <cbc:ID>{data['invoice_number']}</cbc:ID>
    <cbc:IssueDate>{data['issue_date'].strftime('%Y-%m-%d')}</cbc:IssueDate>
    <cbc:DueDate>{data['due_date'].strftime('%Y-%m-%d')}</cbc:DueDate>
    <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
    <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>

    <!-- ÉMETTEUR (Prestataire / Fournisseur) -->
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cbc:EndpointID schemeID="0208">{data['supplier_cbe']}</cbc:EndpointID>
            <cac:PartyIdentification>
                <cbc:ID schemeID="0208">{data['supplier_cbe']}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name>{data['supplier_name']}</cbc:Name>
            </cac:PartyName>
            <cac:PostalAddress>
                <cbc:StreetName>{data['supplier_street']}</cbc:StreetName>
                <cbc:CityName>{data['supplier_city']}</cbc:CityName>
                <cbc:PostalZone>{data['supplier_postal_code']}</cbc:PostalZone>
                <cac:Country>
                    <cbc:IdentificationCode>BE</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyTaxScheme>
                <cbc:CompanyID>{data['supplier_vat']}</cbc:CompanyID>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>{data['supplier_name']}</cbc:RegistrationName>
                <cbc:CompanyID schemeID="0208">{data['supplier_cbe']}</cbc:CompanyID>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingSupplierParty>

    <!-- CLIENT (Donneur d'Ordre B2B) -->
    <cac:AccountingCustomerParty>
        <cac:Party>
            <cbc:EndpointID schemeID="0208">{data['customer_cbe']}</cbc:EndpointID>
            <cac:PartyIdentification>
                <cbc:ID schemeID="0208">{data['customer_cbe']}</cbc:ID>
            </cac:PartyIdentification>
            <cac:PartyName>
                <cbc:Name>{data['customer_name']}</cbc:Name>
            </cac:PartyName>
            <cac:PostalAddress>
                <cbc:StreetName>{data['customer_street']}</cbc:StreetName>
                <cbc:CityName>{data['customer_city']}</cbc:CityName>
                <cbc:PostalZone>{data['customer_postal_code']}</cbc:PostalZone>
                <cac:Country>
                    <cbc:IdentificationCode>BE</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyTaxScheme>
                <cbc:CompanyID>{data['customer_vat']}</cbc:CompanyID>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:PartyTaxScheme>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>{data['customer_name']}</cbc:RegistrationName>
                <cbc:CompanyID schemeID="0208">{data['customer_cbe']}</cbc:CompanyID>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingCustomerParty>

    <!-- MOYEN DE PAIEMENT : VIREMENT BANCAIRE -->
    <cac:PaymentMeans>
        <cbc:PaymentMeansCode>31</cbc:PaymentMeansCode>
        <cbc:PaymentID>{data['invoice_number']}</cbc:PaymentID>
    </cac:PaymentMeans>

    <!-- TOTAL TAXES (TVA Belge 21%) -->
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="EUR">{vat_amount:.2f}</cbc:TaxAmount>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="EUR">{data['amount_htva']:.2f}</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="EUR">{vat_amount:.2f}</cbc:TaxAmount>
            <cac:TaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>{rate_percent}</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
    </cac:TaxTotal>

    <!-- MONTANTS GLOBAUX DE FACTURATION -->
    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID="EUR">{data['amount_htva']:.2f}</cbc:LineExtensionAmount>
        <cbc:TaxExclusiveAmount currencyID="EUR">{data['amount_htva']:.2f}</cbc:TaxExclusiveAmount>
        <cbc:TaxInclusiveAmount currencyID="EUR">{total_ttc:.2f}</cbc:TaxInclusiveAmount>
        <cbc:PayableAmount currencyID="EUR">{total_ttc:.2f}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>

    <!-- LIGNE DE PRESTATION UNIQUE -->
    <cac:InvoiceLine>
        <cbc:ID>1</cbc:ID>
        <cbc:InvoicedQuantity unitCode="C62">1</cbc:InvoicedQuantity>
        <cbc:LineExtensionAmount currencyID="EUR">{data['amount_htva']:.2f}</cbc:LineExtensionAmount>
        <cac:Item>
            <cbc:Description>{data['item_description']}</cbc:Description>
            <cbc:Name>{data['item_description']}</cbc:Name>
            <cac:ClassifiedTaxCategory>
                <cbc:ID>S</cbc:ID>
                <cbc:Percent>{rate_percent}</cbc:Percent>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:ClassifiedTaxCategory>
        </cac:Item>
        <cac:Price>
            <cbc:PriceAmount currencyID="EUR">{data['amount_htva']:.2f}</cbc:PriceAmount>
        </cac:Price>
    </cac:InvoiceLine>
</Invoice>
"""
    return xml_content


def main() -> None:
    parser = argparse.ArgumentParser(description="Générateur de facture électronique Peppol BIS 3.0 UBL 2.1 (Belgique 2026)")
    parser.add_argument("--output-xml", type=str, required=True, help="Chemin du fichier XML à générer")
    parser.add_argument("--invoice-number", type=str, default="FACT-2026-001", help="Numéro officiel de facture")
    parser.add_argument("--client-name", type=str, required=True, help="Raison sociale du client entreprise")
    parser.add_argument("--client-cbe", type=str, default="0123456789", help="Numéro BCE du client (10 chiffres)")
    parser.add_argument("--amount-htva", type=float, required=True, help="Montant HTVA en euros")
    parser.add_argument("--description", type=str, default="Prestations d'installation et suivi système BTP", help="Libellé de prestation")

    args = parser.parse_args()

    cbe_clean = args.client_cbe.replace(".", "").replace(" ", "").replace("BE", "").zfill(10)

    sample_data: PeppolInvoiceData = {
        "invoice_number": args.invoice_number,
        "issue_date": date.today(),
        "due_date": date.today() + timedelta(days=30),
        "supplier_name": "Smart Coop (SC ES) / Bureau Numérique BTP",
        "supplier_cbe": "0459180573",
        "supplier_vat": "BE0459180573",
        "supplier_street": "Rue Émile Féron 70",
        "supplier_city": "Bruxelles",
        "supplier_postal_code": "1060",
        "customer_name": args.client_name,
        "customer_cbe": cbe_clean,
        "customer_vat": f"BE{cbe_clean}",
        "customer_street": "Rue de l'Artisan 12",
        "customer_city": "Liège",
        "customer_postal_code": "4000",
        "item_description": args.description,
        "amount_htva": args.amount_htva,
        "vat_rate": 0.21,
    }

    xml_text = create_peppol_ubl_xml(sample_data)

    with open(args.output_xml, "w", encoding="utf-8") as f:
        f.write(xml_text)

    print("======================================================================")
    print("🇧🇪 FACTURE ÉLECTRONIQUE PEPPOL BIS 3.0 UBL 2.1 GÉNÉRÉE")
    print("======================================================================")
    print(f"Fichier XML    : {args.output_xml}")
    print(f"N° Facture     : {args.invoice_number}")
    print(f"Fournisseur    : {sample_data['supplier_name']} (BCE: {sample_data['supplier_cbe']})")
    print(f"Client B2B     : {args.client_name} (BCE: {cbe_clean})")
    print(f"Montant HTVA   : {args.amount_htva:,.2f} €")
    print(f"TVA (21%)      : {args.amount_htva * 0.21:,.2f} €")
    print(f"Total TTC UBL  : {args.amount_htva * 1.21:,.2f} €")
    print(f"Schéma PEPPOL  : EN 16931 / BIS Billing 3.0 (UBL 2.1)")
    print("======================================================================\n")


if __name__ == "__main__":
    main()
