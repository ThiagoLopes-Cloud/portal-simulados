const XP_KEY      = 'sl_xp'
const LAST_KEY    = (id) => `sl_last_${id}`

const LEVEL_THRESHOLDS = [0, 200, 500, 900, 1400, 2000, 2700, 3500, 4400, 5400]
const XP_PER_AULA = 50

export function getXPData() {
  try {
    return JSON.parse(localStorage.getItem(XP_KEY)) || { xp: 0, completedIds: [] }
  } catch {
    return { xp: 0, completedIds: [] }
  }
}

export function getLevelFromXP(xp) {
  for (let i = LEVEL_THRESHOLDS.length - 1; i >= 0; i--) {
    if (xp >= LEVEL_THRESHOLDS[i]) return i + 1
  }
  return 1
}

export function getNextLevelXP(level) {
  return LEVEL_THRESHOLDS[level] ?? LEVEL_THRESHOLDS[LEVEL_THRESHOLDS.length - 1] + 1200
}

export function getCurrentLevelXP(level) {
  return LEVEL_THRESHOLDS[level - 1] ?? 0
}

export function addAulaXP(aulaId) {
  const data = getXPData()
  if (data.completedIds.includes(aulaId)) {
    return { data, gained: 0, leveled: false }
  }
  const prevLevel = getLevelFromXP(data.xp)
  data.xp += XP_PER_AULA
  data.completedIds.push(aulaId)
  localStorage.setItem(XP_KEY, JSON.stringify(data))
  const newLevel = getLevelFromXP(data.xp)
  return { data, gained: XP_PER_AULA, leveled: newLevel > prevLevel, newLevel }
}

export function getLastViewedAula(trilhaId) {
  const val = localStorage.getItem(LAST_KEY(trilhaId))
  return val ? parseInt(val, 10) : null
}

export function setLastViewedAula(trilhaId, aulaId) {
  localStorage.setItem(LAST_KEY(trilhaId), String(aulaId))
}
