/**
 * Precision Verification Script for Relative-to-Center (RTC) Viewport Rendering.
 */

export function verifyRtcPrecision(): boolean {
  console.log('[*] Vérification de la précision numérique Relative-To-Center (RTC)...');

  // Test de précision Float32 vs Float64
  const worldCoordinateX = 1_000_000.123456789; // 1 million de mm (1 km)
  const cameraX = 1_000_000.0;                   // Caméra à 1 km

  // Cas 1 : Rendu direct sans RTC (Troncature 32 bits)
  const float32Direct = Math.fround(worldCoordinateX);
  const float32Camera = Math.fround(cameraX);
  const naiveOffset = float32Direct - float32Camera;

  // Cas 2 : Rendu RTC (Soustraction 64 bits sur CPU puis envoi 32 bits)
  const rtcOffsetF64 = worldCoordinateX - cameraX;
  const rtcOffsetF32 = Math.fround(rtcOffsetF64);

  const exactValue = 0.123456789;
  const errorNaive = Math.abs(naiveOffset - exactValue);
  const errorRtc = Math.abs(rtcOffsetF32 - exactValue);

  console.log(`    - Coordonnée univers : ${worldCoordinateX} mm`);
  console.log(`    - Erreur naïve (sans RTC) : ${errorNaive.toExponential(4)} mm (Jitter visible !)`);
  console.log(`    - Erreur RTC (CPU Float64) : ${errorRtc.toExponential(4)} mm (Précision chirurgicale)`);

  const passed = errorRtc < 1e-6 && errorNaive > 1e-3;
  console.log(`[+] Résultat du test : ${passed ? 'SUCCÈS' : 'ÉCHEC'}`);
  return passed;
}

if (typeof require !== 'undefined' && require.main === module) {
  verifyRtcPrecision();
}
