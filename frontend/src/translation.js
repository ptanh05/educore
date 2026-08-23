import { createResource } from 'frappe-ui'
import i18n from './i18n'

export default function translationPlugin(app) {
	app.config.globalProperties.__ = translate
	window.__ = translate
	if (!window.translatedMessages) fetchTranslations()
}

function translate(message) {
	let translatedMessages = window.translatedMessages || {}
	let translatedMessage = message
	if (i18n.global.te(message)) {
		translatedMessage = i18n.global.t(message)
	} else if (translatedMessages[message]) {
		translatedMessage = translatedMessages[message]
	}

	const hasPlaceholders = /{\d+}/.test(message)
	if (!hasPlaceholders) {
		return translatedMessage
	}
	return {
		format: function (...args) {
			return translatedMessage.replace(
				/{(\d+)}/g,
				function (match, number) {
					return typeof args[number] != 'undefined'
						? args[number]
						: match
				}
			)
		},
	}
}

function fetchTranslations(lang) {
	createResource({
		url: 'lms.lms.api.get_translations',
		cache: 'translations',
		auto: true,
		transform: (data) => {
			window.translatedMessages = data
		},
	})
}
