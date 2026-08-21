<template>
	<div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
		<div class="sm:mx-auto sm:w-full sm:max-w-md">
			<h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
				{{ __('Admin Access') }}
			</h2>
			<p class="mt-2 text-center text-sm text-gray-600">
				{{ __('Enter administrator API key to continue') }}
			</p>
		</div>

		<div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
			<div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
				<form @submit.prevent="adminLogin" class="space-y-6">
					<div>
						<label for="api_key" class="block text-sm font-medium text-gray-700">
							{{ __('Admin API Key') }}
						</label>
						<div class="mt-1">
							<input
								id="api_key"
								v-model="apiKey"
								type="password"
								required
								class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
								placeholder="Enter Admin API Key"
							/>
						</div>
					</div>

					<div>
						<Button
							class="w-full"
							theme="blue"
							size="lg"
							:loading="adminLoggingIn"
							type="submit"
						>
							{{ __('Login as Admin') }}
						</Button>
					</div>
				</form>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue'
import { Button, call, toast } from 'frappe-ui'

const apiKey = ref('')
const adminLoggingIn = ref(false)

const adminLogin = async () => {
	if (!apiKey.value) {
		toast.error('Please enter the Admin API Key')
		return
	}

	adminLoggingIn.value = true
	try {
		await call('lms.lms.auth.admin_login', { api_key: apiKey.value })
		toast.success('Logged in as Administrator')
		window.location.href = '/lms/unit-dashboard'
	} catch (error) {
		toast.error(error.message || 'Invalid API Key')
	} finally {
		adminLoggingIn.value = false
	}
}
</script>
