import { fileURLToPath } from 'node:url'
import { dirname } from 'node:path'

export const getDirname = (url) => dirname(fileURLToPath(url));