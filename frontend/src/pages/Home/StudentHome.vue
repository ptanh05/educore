<template>
	<div class="space-y-8">
		<!-- 1. Stats Summary Cards -->
		<div class="grid grid-cols-2 md:grid-cols-4 gap-4">
			<div class="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-xl p-4 shadow-sm flex items-center gap-4">
				<div class="p-3 bg-red-50 dark:bg-red-900/30 text-red-600 rounded-lg">
					<span class="lucide-book-open size-6" />
				</div>
				<div>
					<div class="text-xs font-medium text-gray-500 dark:text-gray-400">
						{{ __('Khóa học đang học') }}
					</div>
					<div class="text-xl font-bold text-gray-900 dark:text-white">
						{{ dashboardSummary.data?.stats?.enrolled_courses || 0 }}
					</div>
				</div>
			</div>

			<div class="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-xl p-4 shadow-sm flex items-center gap-4">
				<div class="p-3 bg-blue-50 dark:bg-blue-900/30 text-blue-600 rounded-lg">
					<span class="lucide-layers size-6" />
				</div>
				<div>
					<div class="text-xs font-medium text-gray-500 dark:text-gray-400">
						{{ __('Chương trình / Lớp') }}
					</div>
					<div class="text-xl font-bold text-gray-900 dark:text-white">
						{{ dashboardSummary.data?.stats?.enrolled_batches || 0 }}
					</div>
				</div>
			</div>

			<div class="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-xl p-4 shadow-sm flex items-center gap-4">
				<div class="p-3 bg-emerald-50 dark:bg-emerald-900/30 text-emerald-600 rounded-lg">
					<span class="lucide-check-circle-2 size-6" />
				</div>
				<div>
					<div class="text-xs font-medium text-gray-500 dark:text-gray-400">
						{{ __('Bài học hoàn thành') }}
					</div>
					<div class="text-xl font-bold text-gray-900 dark:text-white">
						{{ dashboardSummary.data?.stats?.completed_lessons || 0 }}
					</div>
				</div>
			</div>

			<div class="bg-white dark:bg-gray-800 border border-gray-100 dark:border-gray-700 rounded-xl p-4 shadow-sm flex items-center gap-4">
				<div class="p-3 bg-amber-50 dark:bg-amber-900/30 text-amber-600 rounded-lg">
					<span class="lucide-award size-6" />
				</div>
				<div>
					<div class="text-xs font-medium text-gray-500 dark:text-gray-400">
						{{ __('Chứng chỉ đã đạt') }}
					</div>
					<div class="text-xl font-bold text-gray-900 dark:text-white">
						{{ dashboardSummary.data?.stats?.certificates || 0 }}
					</div>
				</div>
			</div>
		</div>

		<!-- Empty state if student has no courses -->
		<div
			v-if="dashboardSummary.data?.stats?.enrolled_courses === 0 && !myCourses.loading"
			class="bg-gradient-to-br from-red-500/10 via-amber-500/5 to-transparent border border-red-200/50 dark:border-red-900/40 rounded-2xl p-8 text-center space-y-4"
		>
			<div class="inline-flex p-4 bg-red-100 dark:bg-red-900/40 rounded-full text-red-600">
				<span class="lucide-sparkles size-10" />
			</div>
			<h3 class="text-xl font-bold text-gray-900 dark:text-white">
				{{ __('Chào mừng bạn đến với hệ thống đào tạo Viettel Academy!') }}
			</h3>
			<p class="text-gray-600 dark:text-gray-300 max-w-lg mx-auto text-sm">
				{{ __('Bạn chưa đăng ký khóa học nào. Hãy khám phá kho khóa học đa dạng để nâng cao kỹ năng chuyên môn ngay hôm nay.') }}
			</p>
			<router-link
				:to="{ name: 'Courses' }"
				class="inline-flex items-center gap-2 px-5 py-2.5 bg-red-600 hover:bg-red-700 text-white font-medium text-sm rounded-xl transition-all shadow-md shadow-red-600/20"
			>
				<span class="lucide-compass size-4" />
				{{ __('Khám phá khóa học ngay') }}
			</router-link>
		</div>

		<!-- 2. Continue Learning Section -->
		<div v-if="dashboardSummary.data?.continue_learning" class="space-y-4">
			<div class="flex items-center justify-between">
				<h2 class="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
					<span class="lucide-play-circle size-5 text-red-600" />
					{{ __('Tiếp tục học') }}
				</h2>
			</div>

			<div class="bg-gradient-to-r from-gray-900 via-gray-800 to-gray-900 text-white rounded-2xl p-6 shadow-lg relative overflow-hidden flex flex-col md:flex-row gap-6 items-start md:items-center justify-between">
				<div class="space-y-3 max-w-xl z-10">
					<div class="inline-flex items-center gap-1.5 px-3 py-1 bg-red-600/30 border border-red-500/40 rounded-full text-xs font-semibold text-red-300">
						<span class="lucide-book-open-check size-3.5" />
						{{ __('Khóa học gần nhất') }}
					</div>
					<h3 class="text-2xl font-bold leading-tight">
						{{ dashboardSummary.data.continue_learning.course_title }}
					</h3>
					<div v-if="dashboardSummary.data.continue_learning.lesson_title" class="flex items-center gap-2 text-gray-300 text-sm">
						<span class="lucide-file-text size-4 text-amber-400" />
						<span>
							Bài {{ dashboardSummary.data.continue_learning.chapter_number }}.{{ dashboardSummary.data.continue_learning.lesson_number }}: {{ dashboardSummary.data.continue_learning.lesson_title }}
						</span>
					</div>

					<div class="space-y-1.5 pt-2">
						<div class="flex justify-between text-xs font-medium text-gray-400">
							<span>{{ __('Tiến độ hoàn thành') }}</span>
							<span class="text-red-400 font-bold">{{ dashboardSummary.data.continue_learning.progress }}%</span>
						</div>
						<div class="w-full bg-gray-700 rounded-full h-2 overflow-hidden">
							<div
								class="bg-gradient-to-r from-red-500 to-amber-500 h-2 rounded-full transition-all duration-500"
								:style="{ width: `${dashboardSummary.data.continue_learning.progress}%` }"
							/>
						</div>
					</div>
				</div>

				<div class="z-10 flex flex-col sm:flex-row gap-3 w-full md:w-auto">
					<router-link
						:to="{
							name: 'Lesson',
							params: {
								courseName: dashboardSummary.data.continue_learning.course_name,
								chapterNumber: String(dashboardSummary.data.continue_learning.chapter_number),
								lessonNumber: String(dashboardSummary.data.continue_learning.lesson_number),
							},
						}"
						class="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 bg-red-600 hover:bg-red-500 text-white font-semibold text-sm rounded-xl shadow-lg transition-all"
					>
						<span class="lucide-play size-4 fill-white" />
						{{ __('Học tiếp ngay') }}
					</router-link>
				</div>
			</div>
		</div>

		<!-- Enrolled Courses Grid -->
		<div v-if="myCourses.data?.length" class="space-y-4">
			<div class="flex items-center justify-between">
				<h2 class="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
					<span class="lucide-book-marked size-5 text-red-600" />
					{{ myCourses.data[0].membership ? __('Khóa học của tôi') : __('Khóa học nổi bật') }}
				</h2>
				<router-link :to="{ name: 'Courses' }" class="text-xs font-semibold text-red-600 hover:text-red-700 flex items-center gap-1">
					<span>{{ __('Xem tất cả') }}</span>
					<span class="lucide-arrow-right size-3.5" />
				</router-link>
			</div>

			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
				<router-link
					v-for="course in myCourses.data"
					:key="course.name"
					:to="{ name: 'CourseDetail', params: { courseName: course.name } }"
				>
					<CourseCard :course="course" />
				</router-link>
			</div>
		</div>

		<!-- 3. Section "Việc cần làm" (To-do List) -->
		<div
			v-if="(dashboardSummary.data?.pending_quizzes?.length || dashboardSummary.data?.pending_assignments?.length)"
			class="space-y-4"
		>
			<div class="flex items-center justify-between">
				<h2 class="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
					<span class="lucide-clock-3 size-5 text-amber-500" />
					{{ __('Việc cần làm & Bài tập') }}
				</h2>
			</div>

			<div class="grid grid-cols-1 md:grid-cols-2 gap-4">
				<!-- Pending Quizzes -->
				<div
					v-for="quiz in dashboardSummary.data.pending_quizzes"
					:key="quiz.name"
					class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-4 flex items-center justify-between gap-4 shadow-sm hover:border-amber-400 transition-colors"
				>
					<div class="space-y-1">
						<div class="inline-flex items-center gap-1 text-[11px] font-semibold text-amber-600 dark:text-amber-400 bg-amber-50 dark:bg-amber-900/30 px-2 py-0.5 rounded">
							<span class="lucide-help-circle size-3" />
							Quiz cần làm
						</div>
						<div class="font-bold text-gray-900 dark:text-white text-sm">
							{{ quiz.title }}
						</div>
						<div class="text-xs text-gray-500 dark:text-gray-400">
							{{ quiz.course_title }}
						</div>
					</div>
					<router-link
						:to="{ name: 'QuizPage', params: { quizID: quiz.name } }"
						class="shrink-0 px-3 py-1.5 bg-amber-500 hover:bg-amber-600 text-white font-medium text-xs rounded-lg transition-colors"
					>
						{{ __('Làm Quiz') }}
					</router-link>
				</div>

				<!-- Pending Assignments -->
				<div
					v-for="assignment in dashboardSummary.data.pending_assignments"
					:key="assignment.name"
					class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-4 flex items-center justify-between gap-4 shadow-sm hover:border-blue-400 transition-colors"
				>
					<div class="space-y-1">
						<div class="inline-flex items-center gap-1 text-[11px] font-semibold text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 px-2 py-0.5 rounded">
							<span class="lucide-file-signature size-3" />
							Assignment cần nộp
						</div>
						<div class="font-bold text-gray-900 dark:text-white text-sm">
							{{ assignment.title }}
						</div>
						<div class="text-xs text-gray-500 dark:text-gray-400">
							{{ assignment.course_title }}
						</div>
					</div>
					<router-link
						:to="{
							name: 'AssignmentSubmission',
							params: {
								assignmentID: assignment.name,
								submissionName: assignment.submission_name || 'new',
							},
						}"
						class="shrink-0 px-3 py-1.5 bg-blue-600 hover:bg-blue-700 text-white font-medium text-xs rounded-lg transition-colors"
					>
						{{ __('Nộp bài') }}
					</router-link>
				</div>
			</div>
		</div>

		<!-- 4. Section "Lịch sắp tới" (Upcoming Schedule & Live Classes) -->
		<div class="space-y-4">
			<UpcomingEvaluations :forHome="true" />

			<div v-if="myLiveClasses.data?.length" class="space-y-3">
				<div class="flex items-center justify-between">
					<h2 class="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
						<span class="lucide-video size-5 text-red-600" />
						{{ __('Lớp học trực tuyến sắp tới') }}
					</h2>
				</div>

				<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
					<div
						v-for="cls in myLiveClasses.data"
						:key="cls.name"
						class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl p-4 space-y-3 shadow-sm hover:border-red-300 transition-colors"
					>
						<div>
							<div class="font-bold text-gray-900 dark:text-white text-base">
								{{ cls.title }}
							</div>
							<div class="text-xs text-gray-500 dark:text-gray-400 line-clamp-2 mt-1">
								{{ cls.description }}
							</div>
						</div>

						<div class="space-y-1.5 text-xs text-gray-600 dark:text-gray-300 pt-2 border-t border-gray-100 dark:border-gray-700">
							<div class="flex items-center gap-2">
								<span class="lucide-calendar size-3.5 text-red-500" />
								<span>{{ dayjs(cls.date).format('DD MMMM YYYY') }}</span>
							</div>
							<div class="flex items-center gap-2">
								<span class="lucide-clock size-3.5 text-red-500" />
								<span>
									{{ formatTime(cls.time) }} -
									{{ dayjs(getClassEnd(cls)).format('HH:mm A') }}
								</span>
							</div>
						</div>

						<div v-if="canAccessClass(cls)" class="pt-2">
							<a
								:href="cls.join_url"
								target="_blank"
								class="w-full inline-flex items-center justify-center gap-2 px-3 py-2 bg-red-600 hover:bg-red-700 text-white font-medium text-xs rounded-lg transition-colors shadow-sm"
							>
								<span class="lucide-video size-3.5" />
								{{ __('Vào lớp ngay') }}
							</a>
						</div>
						<div v-else-if="hasClassEnded(cls)" class="pt-2 text-xs text-amber-600 flex items-center gap-1">
							<span class="lucide-info size-3.5" />
							<span>{{ __('Lớp học đã kết thúc') }}</span>
						</div>
					</div>
				</div>
			</div>
		</div>

		<!-- Enrolled Batches -->
		<div v-if="myBatches.data?.length" class="space-y-4">
			<div class="flex items-center justify-between">
				<h2 class="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
					<span class="lucide-users size-5 text-red-600" />
					{{
						myBatches.data?.[0].students?.includes(user.data?.name)
							? __('Chương trình đang tham gia')
							: __('Chương trình sắp khai giảng')
					}}
				</h2>
				<router-link :to="{ name: 'Batches' }" class="text-xs font-semibold text-red-600 hover:text-red-700 flex items-center gap-1">
					<span>{{ __('Xem tất cả') }}</span>
					<span class="lucide-arrow-right size-3.5" />
				</router-link>
			</div>

			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
				<router-link
					v-for="batch in myBatches.data"
					:key="batch.name"
					:to="{ name: 'BatchDetail', params: { batchName: batch.name } }"
				>
					<BatchCard :batch="batch" />
				</router-link>
			</div>
		</div>

		<!-- 5. Section "Chứng chỉ & Thành tích" -->
		<div v-if="dashboardSummary.data?.certificates?.length" class="space-y-4">
			<div class="flex items-center justify-between">
				<h2 class="text-lg font-bold text-gray-900 dark:text-white flex items-center gap-2">
					<span class="lucide-award size-5 text-emerald-600" />
					{{ __('Chứng chỉ đã đạt') }}
				</h2>
				<router-link
					:to="{ name: 'ProfileCertificates', params: { username: user.data?.username || '' } }"
					class="text-xs font-semibold text-emerald-600 hover:text-emerald-700 flex items-center gap-1"
				>
					<span>{{ __('Xem tất cả chứng chỉ') }}</span>
					<span class="lucide-arrow-right size-3.5" />
				</router-link>
			</div>

			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
				<div
					v-for="cert in dashboardSummary.data.certificates"
					:key="cert.name"
					class="bg-white dark:bg-gray-800 border border-emerald-100 dark:border-emerald-900/30 rounded-xl p-4 flex items-center justify-between gap-4 shadow-sm"
				>
					<div class="space-y-1">
						<div class="font-bold text-gray-900 dark:text-white text-sm line-clamp-1">
							{{ cert.course_title || cert.batch_title || __('Chứng chỉ Viettel Academy') }}
						</div>
						<div class="text-xs text-gray-500 dark:text-gray-400">
							Cấp ngày: {{ dayjs(cert.issue_date).format('DD/MM/YYYY') }}
						</div>
					</div>
					<router-link
						v-if="cert.course"
						:to="{ name: 'CourseCertification', params: { courseName: cert.course } }"
						class="shrink-0 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-xs rounded-lg transition-colors flex items-center gap-1"
					>
						<span class="lucide-eye size-3.5" />
						{{ __('Xem') }}
					</router-link>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { inject } from 'vue'
import { createResource } from 'frappe-ui'
import { formatTime } from '@/utils'
import CourseCard from '@/components/CourseCard.vue'
import BatchCard from '@/pages/Batches/components/BatchCard.vue'
import UpcomingEvaluations from '@/components/UpcomingEvaluations.vue'

const dayjs = inject<any>('$dayjs')
const user = inject<any>('$user')

const props = defineProps<{
	myLiveClasses: any
}>()

const dashboardSummary = createResource({
	url: 'lms.lms.api.get_student_dashboard',
	auto: true,
})

const myCourses = createResource({
	url: 'lms.lms.api.get_my_courses',
	auto: true,
})

const myBatches = createResource({
	url: 'lms.lms.api.get_my_batches',
	auto: true,
})

const getClassEnd = (cls: { date: string; time: string; duration: number }) => {
	const classStart = new Date(`${cls.date}T${cls.time}`)
	return new Date(classStart.getTime() + cls.duration * 60000)
}

const canAccessClass = (cls: {
	date: string
	time: string
	duration: number
}) => {
	if (cls.date < dayjs().format('YYYY-MM-DD')) return false
	if (cls.date > dayjs().format('YYYY-MM-DD')) return false
	if (hasClassEnded(cls)) return false
	return true
}

const hasClassEnded = (cls: {
	date: string
	time: string
	duration: number
}) => {
	const classEnd = getClassEnd(cls)
	const now = new Date()
	return now > classEnd
}
</script>
