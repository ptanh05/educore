<template>
	<div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8 relative overflow-hidden">
		<!-- Background decorations -->
		<div class="absolute inset-0 z-0 opacity-20 pointer-events-none">
			<div class="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-viettel-red mix-blend-multiply filter blur-3xl opacity-30 animate-blob"></div>
			<div class="absolute -bottom-24 -right-24 w-96 h-96 rounded-full bg-red-300 mix-blend-multiply filter blur-3xl opacity-30 animate-blob animation-delay-2000"></div>
		</div>

		<div class="sm:mx-auto sm:w-full sm:max-w-md z-10">
			<div class="flex justify-center mb-6">
				<!-- Brand Logo -->
				<img src="/viettel_academy_logo.svg" alt="Viettel Academy" class="h-12" @error="handleLogoError" ref="logoImg" />
			</div>
			<h2 class="mt-2 text-center text-3xl font-extrabold text-gray-900 tracking-tight">
				{{ __('Chào mừng đến với Viettel Academy') }}
			</h2>
			<p class="mt-2 text-center text-sm text-gray-600">
				{{ __subtitle }}
			</p>
		</div>

		<div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md z-10 transition-all duration-300 transform" :class="{'scale-95 opacity-50': processing}">
			<div class="bg-white py-8 px-4 shadow-xl sm:rounded-xl sm:px-10 border border-gray-100">
				<!-- Success state for verification/reset -->
				<div v-if="successMessage" class="rounded-md bg-green-50 p-4 mb-6 border border-green-200">
					<div class="flex">
						<div class="flex-shrink-0">
							<svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
								<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
							</svg>
						</div>
						<div class="ml-3">
							<p class="text-sm font-medium text-green-800">{{ successMessage }}</p>
						</div>
					</div>
				</div>

				<!-- Verify account success (from URL) -->
				<div v-if="isVerified" class="rounded-md bg-green-50 p-4 mb-6 border border-green-200">
					<div class="flex">
						<div class="flex-shrink-0">
							<svg class="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
								<path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
							</svg>
						</div>
						<div class="ml-3">
							<p class="text-sm font-medium text-green-800">{{ __('Tài khoản đã được xác thực thành công. Vui lòng đăng nhập.') }}</p>
						</div>
					</div>
				</div>

				<form @submit.prevent="handleUserSubmit" class="space-y-5">
					<div v-if="userMode === 'signup'">
						<label for="fullName" class="block text-sm font-medium text-gray-700">
							{{ __('Họ và tên') }} <span class="text-viettel-red">*</span>
						</label>
						<div class="mt-1">
							<input
								id="fullName"
								v-model="fullName"
								type="text"
								required
								class="appearance-none block w-full px-3 py-2.5 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-viettel-red focus:border-viettel-red sm:text-sm transition-colors"
								placeholder="Nguyễn Văn A"
							/>
						</div>
					</div>

					<div>
						<label for="email" class="block text-sm font-medium text-gray-700">
							{{ __('Địa chỉ Email') }} <span class="text-viettel-red">*</span>
						</label>
						<div class="mt-1">
							<input
								id="email"
								v-model="email"
								type="email"
								autocomplete="email"
								required
								class="appearance-none block w-full px-3 py-2.5 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-viettel-red focus:border-viettel-red sm:text-sm transition-colors"
								placeholder="you@example.com"
							/>
						</div>
					</div>

					<div v-if="userMode !== 'forgot_password'">
						<div class="flex items-center justify-between">
							<label for="password" class="block text-sm font-medium text-gray-700">
								{{ __('Mật khẩu') }} <span class="text-viettel-red">*</span>
							</label>
							<div class="text-sm" v-if="userMode === 'login'">
								<button type="button" @click="userMode = 'forgot_password'" class="font-medium text-viettel-red hover:text-viettel-red-dark transition-colors">
									{{ __('Quên mật khẩu?') }}
								</button>
							</div>
						</div>
						<div class="mt-1 relative">
							<input
								id="password"
								v-model="password"
								:type="showPassword ? 'text' : 'password'"
								autocomplete="current-password"
								required
								class="appearance-none block w-full px-3 py-2.5 border border-gray-300 rounded-lg shadow-sm placeholder-gray-400 focus:outline-none focus:ring-viettel-red focus:border-viettel-red sm:text-sm transition-colors pr-10"
								placeholder="••••••••"
							/>
							<button type="button" @click="showPassword = !showPassword" class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-500">
								<!-- Eye icon -->
								<svg v-if="!showPassword" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
								</svg>
								<svg v-else class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.542-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.542 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
								</svg>
							</button>
						</div>
						<p v-if="userMode === 'signup'" class="mt-2 text-xs text-gray-500 leading-tight">
							{{ __('Mật khẩu cần tối thiểu 8 ký tự, bao gồm ít nhất 1 chữ hoa và 1 chữ số.') }}
						</p>
					</div>

					<div class="pt-2">
						<button
							class="w-full flex justify-center py-2.5 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-viettel-red hover:bg-viettel-red-dark focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-viettel-red transition-colors"
							:disabled="processing"
							type="submit"
						>
							<svg v-if="processing" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
							</svg>
							{{ submitButtonText }}
						</button>
					</div>
				</form>

				<div v-if="userMode === 'login' || userMode === 'signup'" class="mt-6">
					<div class="relative">
						<div class="absolute inset-0 flex items-center">
							<div class="w-full border-t border-gray-200"></div>
						</div>
						<div class="relative flex justify-center text-sm">
							<span class="px-2 bg-white text-gray-500">
								{{ __('Hoặc tiếp tục với') }}
							</span>
						</div>
					</div>

					<div class="mt-6">
						<button
							@click.prevent="loginWithGoogle"
							:disabled="googleLoggingIn"
							class="w-full flex justify-center py-2.5 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-200"
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

				<div class="mt-8 text-center text-sm">
					<button
						v-if="userMode === 'login'"
						@click="userMode = 'signup'; successMessage = ''"
						class="font-medium text-viettel-red hover:text-viettel-red-dark transition-colors"
					>
						{{ __("Chưa có tài khoản? Đăng ký ngay") }}
					</button>
					<button
						v-else
						@click="userMode = 'login'; successMessage = ''"
						class="font-medium text-viettel-red hover:text-viettel-red-dark transition-colors"
					>
						{{ __("Đã có tài khoản? Đăng nhập") }}
					</button>
					
					<div v-if="userMode === 'login'" class="mt-3">
						<button
							@click="resendVerification"
							class="text-xs text-gray-500 hover:text-gray-700 underline"
						>
							{{ __("Chưa nhận được email xác thực? Gửi lại") }}
						</button>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { call, toast } from 'frappe-ui'

const userMode = ref('login') // 'login', 'signup', or 'forgot_password'
const showPassword = ref(false)

const fullName = ref('')
const email = ref('')
const password = ref('')
const processing = ref(false)
const successMessage = ref('')
const isVerified = ref(false)

const logoImg = ref(null)

onMounted(() => {
	// Check for verification success in URL
	const urlParams = new URLSearchParams(window.location.search);
	if (urlParams.get('verified') === '1') {
		isVerified.value = true;
		// Clean up URL without page reload
		window.history.replaceState({}, document.title, window.location.pathname);
	}
})

const handleLogoError = () => {
	if (logoImg.value) {
		logoImg.value.src = '/assets/lms/images/lms-logo.png' // Fallback
	}
}

const __subtitle = computed(() => {
	if (userMode.value === 'login') return __('Đăng nhập để tiếp tục học tập')
	if (userMode.value === 'signup') return __('Tạo tài khoản mới')
	if (userMode.value === 'forgot_password') return __('Khôi phục mật khẩu của bạn')
	return ''
})

const submitButtonText = computed(() => {
	if (userMode.value === 'login') return __('Đăng nhập')
	if (userMode.value === 'signup') return __('Đăng ký')
	if (userMode.value === 'forgot_password') return __('Gửi link khôi phục')
	return ''
})

const handleUserSubmit = async () => {
	if (!email.value) {
		toast.error(__('Vui lòng nhập email'))
		return
	}
	
	if (userMode.value !== 'forgot_password' && !password.value) {
		toast.error(__('Vui lòng nhập mật khẩu'))
		return
	}
	
	if (userMode.value === 'signup' && !fullName.value) {
		toast.error(__('Vui lòng nhập họ và tên'))
		return
	}

	processing.value = true
	successMessage.value = ''
	isVerified.value = false
	
	try {
		if (userMode.value === 'login') {
			await call('login', {
				usr: email.value,
				pwd: password.value
			})
			toast.success(__('Đăng nhập thành công'))
			window.location.href = '/lms/courses'
		} else if (userMode.value === 'signup') {
			const res = await call('lms.lms.auth.sign_up', {
				email: email.value,
				full_name: fullName.value,
				password: password.value
			})
			successMessage.value = res.message || __('Tạo tài khoản thành công! Vui lòng kiểm tra email để xác thực.')
			// Optional: switch back to login after signup
			userMode.value = 'login'
			password.value = ''
		} else if (userMode.value === 'forgot_password') {
			const res = await call('lms.lms.auth.forgot_password', {
				email: email.value
			})
			successMessage.value = res.message || __('Link khôi phục mật khẩu đã được gửi, vui lòng kiểm tra email.')
			userMode.value = 'login'
		}
	} catch (error) {
		toast.error(error.message || (userMode.value === 'login' ? __('Thông tin đăng nhập không hợp lệ hoặc tài khoản chưa xác thực') : __('Có lỗi xảy ra, vui lòng thử lại')))
	} finally {
		processing.value = false
	}
}

const resendVerification = async () => {
	if (!email.value) {
		toast.error(__('Vui lòng nhập email của bạn ở trên để nhận lại link xác thực'))
		return
	}
	processing.value = true
	try {
		const res = await call('lms.lms.auth.resend_verification', {
			email: email.value
		})
		toast.success(res.message || __('Đã gửi lại link xác thực'))
	} catch (error) {
		toast.error(error.message || __('Có lỗi xảy ra, vui lòng thử lại'))
	} finally {
		processing.value = false
	}
}

const googleLoggingIn = ref(false)
const loginWithGoogle = async () => {
	googleLoggingIn.value = true
	try {
		const url = await call('lms.lms.auth.get_google_login_url')
		window.location.href = url
	} catch (error) {
		toast.error(error.message || __('Đăng nhập Google chưa được cấu hình.'))
	} finally {
		googleLoggingIn.value = false
	}
}
</script>

<style>
@keyframes blob {
  0% { transform: translate(0px, 0px) scale(1); }
  33% { transform: translate(30px, -50px) scale(1.1); }
  66% { transform: translate(-20px, 20px) scale(0.9); }
  100% { transform: translate(0px, 0px) scale(1); }
}
.animate-blob {
  animation: blob 7s infinite;
}
.animation-delay-2000 {
  animation-delay: 2s;
}
</style>
