<template>
	<div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
		<div class="sm:mx-auto sm:w-full sm:max-w-md">
			<h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
				{{ __('Welcome to Educore') }}
			</h2>
			<p class="mt-2 text-center text-sm text-gray-600">
				{{ __('Sign in to your account') }}
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
							{{ __('User (OTP)') }}
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

				<div v-if="activeTab === 'user'">
					<div v-if="!otpSent" class="space-y-6">
						<div>
							<label for="email" class="block text-sm font-medium text-gray-700">
								{{ __('Email address') }}
							</label>
							<div class="mt-1">
								<input
									id="email"
									v-model="email"
									name="email"
									type="email"
									autocomplete="email"
									required
									class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
									placeholder="you@gmail.com"
								/>
							</div>
						</div>

						<div>
							<Button
								class="w-full"
								theme="blue"
								size="lg"
								:loading="sendingOtp"
								@click="sendOtp"
							>
								{{ __('Send OTP') }}
							</Button>
						</div>
					</div>

					<div v-else class="space-y-6">
						<div>
							<label for="otp" class="block text-sm font-medium text-gray-700">
								{{ __('Enter OTP Code') }}
							</label>
							<p class="text-xs text-gray-500 mt-1 mb-2">We sent a verification code to {{ email }}</p>
							<div class="mt-1">
								<input
									id="otp"
									v-model="otp"
									name="otp"
									type="text"
									required
									class="appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
									placeholder="123456"
								/>
							</div>
						</div>

						<div class="flex flex-col gap-3">
							<Button
								class="w-full"
								theme="blue"
								size="lg"
								:loading="verifyingOtp"
								@click="verifyOtpAndLogin"
							>
								{{ __('Verify and Login') }}
							</Button>
							<Button
								class="w-full"
								variant="ghost"
								@click="otpSent = false"
							>
								{{ __('Use a different email') }}
							</Button>
						</div>
					</div>
				</div>

				<div v-if="activeTab === 'admin'" class="space-y-6">
					<div>
						<label for="api_key" class="block text-sm font-medium text-gray-700">
							{{ __('Admin API Key') }}
						</label>
						<div class="mt-1">
							<input
								id="api_key"
								v-model="apiKey"
								name="api_key"
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
							@click="adminLogin"
						>
							{{ __('Login as Admin') }}
						</Button>
					</div>
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

const email = ref('')
const otp = ref('')
const otpSent = ref(false)
const sendingOtp = ref(false)
const verifyingOtp = ref(false)

const apiKey = ref('')
const adminLoggingIn = ref(false)

const sendOtp = async () => {
	if (!email.value) {
		toast.error('Please enter your email')
		return
	}
	if (!email.value.includes('@')) {
		toast.error('Please enter a valid email address')
		return
	}
	
	sendingOtp.value = true
	try {
		await call('lms.lms.auth.send_otp', { email: email.value })
		toast.success('OTP sent successfully')
		otpSent.value = true
	} catch (error) {
		toast.error(error.message || 'Failed to send OTP')
	} finally {
		sendingOtp.value = false
	}
}

const verifyOtpAndLogin = async () => {
	if (!otp.value) {
		toast.error('Please enter the OTP code')
		return
	}
	
	verifyingOtp.value = true
	try {
		await call('lms.lms.auth.verify_otp_and_login', { 
			email: email.value, 
			otp: otp.value 
		})
		toast.success('Logged in successfully')
		window.location.href = '/lms/courses'
	} catch (error) {
		toast.error(error.message || 'Invalid OTP')
	} finally {
		verifyingOtp.value = false
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
</script>
