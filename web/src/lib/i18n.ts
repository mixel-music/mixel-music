import { browser } from '$app/environment'
import { init, register } from 'svelte-i18n'

const defaultLocale = 'ko'

register('en', () => import('./i18n/en.json'))
register('ko', () => import('./i18n/ko.json'))

init({
	fallbackLocale: defaultLocale,
	initialLocale: browser ? window.navigator.language : defaultLocale,
})
