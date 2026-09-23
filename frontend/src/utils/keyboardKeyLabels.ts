const KEY_CODE_LABELS: Record<string, string> = {
  Space: 'Espacio',
  Enter: 'Enter',
  Tab: 'Tab',
  Escape: 'Escape',
  ControlLeft: 'Ctrl izquierdo',
  ControlRight: 'Ctrl derecho',
  AltLeft: 'Alt izquierdo',
  AltRight: 'Alt derecho',
  ShiftLeft: 'Shift izquierdo',
  ShiftRight: 'Shift derecho',
  ArrowUp: 'Flecha arriba',
  ArrowDown: 'Flecha abajo',
  ArrowLeft: 'Flecha izquierda',
  ArrowRight: 'Flecha derecha',
  Backspace: 'Backspace',
  CapsLock: 'Bloq Mayús',
}

const LETTER_KEY_PATTERN = /^Key([A-Z])$/
const DIGIT_KEY_PATTERN = /^Digit([0-9])$/
const FUNCTION_KEY_PATTERN = /^F([1-9]|1[0-9]|2[0-4])$/
const NUMPAD_KEY_PATTERN = /^Numpad([0-9])$/

/**
 * Traduce un event.code del navegador a una etiqueta legible en español para
 * mostrar en la UI. Es el único lugar donde vive este formateo — tanto
 * EventConfigScreen como el panel del moderador lo reutilizan.
 */
export function formatKeyCodeLabel(code: string): string {
  const letterMatch = code.match(LETTER_KEY_PATTERN)
  if (letterMatch) {
    return letterMatch[1]
  }

  const digitMatch = code.match(DIGIT_KEY_PATTERN)
  if (digitMatch) {
    return digitMatch[1]
  }

  const numpadMatch = code.match(NUMPAD_KEY_PATTERN)
  if (numpadMatch) {
    return `Num ${numpadMatch[1]}`
  }

  if (FUNCTION_KEY_PATTERN.test(code)) {
    return code
  }

  return KEY_CODE_LABELS[code] ?? code
}
