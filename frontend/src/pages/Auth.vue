<template>
	<div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
		<div class="sm:mx-auto sm:w-full sm:max-w-md">
			<h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
				{{ __('Welcome to Educore') }}
			</h2>
			<p class="mt-2 text-center text-sm text-gray-600">
				{{ activeTab === 'user' ? __('Sign in or create an account') : __('Admin Access') }}
			</p>
		</div>

		<div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
			<div class="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
				<div class="mb-6">
					<div class="flex space-x-4 border-b border-gray-200">
						<button
							@click="activeTab = 'user'"
							:class="[
								activeTab === 'user' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
								'whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm flex-1'
							]"
						>
							{{ __('User') }}
						</button>
						<button
							@click="activeTab = 'admin'"
							:class="[
								activeTab === 'admin' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
								'whitespace-nowrap pb-4 px-1 border-b-2 font-medium text-sm flex-1'
							]"
						>
							{{ __('Admin (Key)') }}
						</button>
					</div>
				</div>

				<!-- User Tab -->
				<div v-if="activeTab === 'user'">
					<form @submit.prevent="handleUserSubmit" class="space-y-6">
						<div v-if="userMode === 'signup'">
							<label for="fullName" class="block text-sm font-medium text-gray-700">
								{{ __('Full Name') }}
							</label>
							<div class="mt-1">
								<input
									id="fullName"
									v-model="fullName"
									type="text"
									required
									class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
									placeholder="John Doe"
								/>
							</div>
						</div>

						<div>
							<label for="email" class="block text-sm font-medium text-gray-700">
								{{ __('Email address') }}
							</label>
							<div class="mt-1">
								<input
									id="email"
									v-model="email"
									type="email"
									autocomplete="email"
									required
									class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
									placeholder="you@example.com"
								/>
							</div>
						</div>

						<div>
							<label for="password" class="block text-sm font-medium text-gray-700">
								{{ __('Password') }}
							</label>
							<div class="mt-1">
								<input
									id="password"
									v-model="password"
									type="password"
									autocomplete="current-password"
									required
									class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
									placeholder="••••••••"
								/>
							</div>
						</div>

						<div>
							<Button
								class="w-full"
								theme="blue"
								size="lg"
								:loading="processing"
								type="submit"
							>
								{{ userMode === 'login' ? __('Sign In') : __('Sign Up') }}
							</Button>
						</div>
					</form>

					<div class="mt-6">
						<div class="relative">
							<div class="absolute inset-0 flex items-center">
								<div class="w-full border-t border-gray-300"></div>
							</div>
							<div class="relative flex justify-center text-sm">
								<span class="px-2 bg-white text-gray-500">
									{{ __('Or continue with') }}
								</span>
							</div>
						</div>

						<div class="mt-6">
							<button
								@click.prevent="loginWithGoogle"
								:disabled="googleLoggingIn"
								class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50"
							>
								<svg class="w-5 h-5 mr-2" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
									<path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
									<path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
									<path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
									<path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
								</svg>
								{{ __('Google') }}
							</button>
						</div>
					</div>

					<div class="mt-6 text-center text-sm">
						<button
							v-if="userMode === 'login'"
							@click="userMode = 'signup'"
							class="font-medium text-blue-600 hover:text-blue-500"
						>
							{{ __("Don't have an account? Sign Up") }}
						</button>
						<button
							v-else
							@click="userMode = 'login'"
							class="font-medium text-blue-600 hover:text-blue-500"
						>
							{{ __("Already have an account? Sign In") }}
						</button>
					</div>
				</div>

				<!-- Admin Tab -->
				<div v-if="activeTab === 'admin'" class="space-y-6">
					<form @submit.prevent="adminLogin">
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

						<div class="mt-6">
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
	</div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { Button, call, toast } from 'frappe-ui'

const router = useRouter()

const activeTab = ref('user') // 'user' or 'admin'
const userMode = ref('login') // 'login' or 'signup'

const fullName = ref('')
const email = ref('')
const password = ref('')
const processing = ref(false)

const apiKey = ref('')
const adminLoggingIn = ref(false)

const handleUserSubmit = async () => {
	if (!email.value || !password.value) {
		toast.error('Please fill in all fields')
		return
	}
	if (userMode.value === 'signup' && !fullName.value) {
		toast.error('Please enter your full name')
		return
	}
	
	processing.value = true
	try {
		if (userMode.value === 'login') {
			await call('login', { 
				usr: email.value, 
				pwd: password.value 
			})
			toast.success('Logged in successfully')
		} else {
			await call('lms.lms.auth.sign_up', { 
				email: email.value, 
				full_name: fullName.value,
				password: password.value
			})
			toast.success('Account created successfully')
		}
		window.location.href = '/lms/courses'
	} catch (error) {
		toast.error(error.message || (userMode.value === 'login' ? 'Invalid credentials' : 'Signup failed'))
	} finally {
		processing.value = false
	}
}

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

const googleLoggingIn = ref(false)
const loginWithGoogle = async () => {
	googleLoggingIn.value = true
	try {
		const url = await call('lms.lms.auth.get_google_login_url')
		window.location.href = url
	} catch (error) {
		toast.error(error.message || 'Google Login is not configured.')
	} finally {
		googleLoggingIn.value = false
	}
}
</script>
