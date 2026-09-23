export interface EventConfig {
  correct_answer_points: number
  response_time_seconds: number
  player_1_key: string
  player_2_key: string
  player_3_key: string
  player_4_key: string
}

// Campos como texto mientras el formulario se edita, para permitir borrar el
// input por completo o escribir un número nuevo sin que un 0 forzado por la
// conversión a número quede delante de lo que el usuario está tecleando.
// Las teclas ya llegan como texto (event.code) sin necesitar esa conversión.
export interface EventConfigFormData {
  correct_answer_points: string
  response_time_seconds: string
  player_1_key: string
  player_2_key: string
  player_3_key: string
  player_4_key: string
}

export function eventConfigToFormData(config: EventConfig): EventConfigFormData {
  return {
    correct_answer_points: String(config.correct_answer_points),
    response_time_seconds: String(config.response_time_seconds),
    player_1_key: config.player_1_key,
    player_2_key: config.player_2_key,
    player_3_key: config.player_3_key,
    player_4_key: config.player_4_key,
  }
}
