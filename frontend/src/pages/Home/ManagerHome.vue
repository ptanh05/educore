<template>
	<div class="w-full px-5 pt-5 pb-10">
		<div class="flex flex-col sm:flex-row items-start sm:items-center justify-between mb-6 gap-4">
			<div class="text-2xl font-bold text-ink-gray-9">
				{{ __('Dashboard Quản Lý Đơn Vị') }}
			</div>
			<div class="flex flex-wrap items-center gap-3">
				<!-- Course filter -->
				<select v-model="selectedCourse" class="form-input text-sm rounded-md border-outline-gray-3 bg-surface-white text-ink-gray-7 h-9 px-3 min-w-[200px]">
					<option value="">{{ __('Tất cả khóa học') }}</option>
					<option v-for="course in courses?.data" :key="course.name" :value="course.name">
						{{ course.title }}
					</option>
				</select>
				
				<Button size="md" variant="solid" @click="exportReport">
					<template #prefix><span class="lucide-download size-4" /></template>
					{{ __('Export Báo Cáo') }}
				</Button>
			</div>
		</div>

		<div v-if="dashboardStats.loading" class="flex flex-1 items-center justify-center py-20">
			<LoadingIndicator class="size-5 text-ink-gray-5" />
		</div>
		<div v-else-if="dashboardStats.data" class="space-y-8">
			<!-- Stats -->
			<div class="grid grid-cols-2 md:grid-cols-6 gap-5">
				<div class="border rounded-md p-4 flex flex-col justify-between hover:border-outline-gray-3 bg-surface-white shadow-sm">
					<div class="text-ink-gray-5 text-sm font-medium mb-1">{{ __('Tổng Nhân Sự') }}</div>
					<div class="text-2xl font-semibold text-ink-gray-9">{{ dashboardStats.data.total_users }}</div>
				</div>
				<div class="border rounded-md p-4 flex flex-col justify-between hover:border-outline-gray-3 bg-surface-white shadow-sm">
					<div class="text-ink-gray-5 text-sm font-medium mb-1">{{ __('Tỷ Lệ Hoàn Thành') }}</div>
					<div class="text-2xl font-semibold text-ink-gray-9">{{ dashboardStats.data.completion_rate }}%</div>
				</div>
				<div class="border rounded-md p-4 flex flex-col justify-between hover:border-outline-gray-3 bg-surface-white shadow-sm">
					<div class="text-ink-gray-5 text-sm font-medium mb-1">{{ __('Chưa Hoàn Thành') }}</div>
					<div class="text-2xl font-semibold text-ink-amber-6">{{ dashboardStats.data.incomplete_users.length }}</div>
				</div>
				<div class="border rounded-md p-4 flex flex-col justify-between hover:border-outline-gray-3 bg-surface-white shadow-sm">
					<div class="text-ink-gray-5 text-sm font-medium mb-1">{{ __('Quá Hạn') }}</div>
					<div class="text-2xl font-semibold text-ink-red-6">{{ dashboardStats.data.overdue_users.length }}</div>
				</div>
				<div class="border rounded-md p-4 flex flex-col justify-between hover:border-outline-gray-3 bg-surface-white shadow-sm">
					<div class="text-ink-gray-5 text-sm font-medium mb-1">{{ __('Điểm TB (Quiz)') }}</div>
					<div class="text-2xl font-semibold text-ink-gray-9">{{ dashboardStats.data.average_score }}%</div>
				</div>
				<div class="border rounded-md p-4 flex flex-col justify-between hover:border-outline-gray-3 bg-surface-white shadow-sm">
					<div class="text-ink-gray-5 text-sm font-medium mb-1">{{ __('Chứng Chỉ Đã Cấp') }}</div>
					<div class="text-2xl font-semibold text-ink-gray-9">{{ dashboardStats.data.certificates_issued }}</div>
				</div>
			</div>

			<!-- Lists -->
			<div class="grid grid-cols-1 md:grid-cols-2 gap-8">
				<!-- Incomplete Users -->
				<div class="border rounded-md overflow-hidden bg-surface-white shadow-sm">
					<div class="bg-surface-gray-2 px-4 py-3 border-b text-ink-gray-9 font-semibold">
						{{ __('Nhân Sự Chưa Hoàn Thành') }}
					</div>
					<div class="p-4" v-if="dashboardStats.data.incomplete_users.length === 0">
						<div class="text-ink-gray-5 text-sm">{{ __('Tất cả nhân sự đã hoàn thành khóa học.') }}</div>
					</div>
					<div class="max-h-96 overflow-y-auto" v-else>
						<table class="w-full text-left border-collapse text-sm">
							<thead class="bg-surface-gray-1 sticky top-0 z-10">
								<tr>
									<th class="p-3 border-b font-medium text-ink-gray-5 whitespace-nowrap">{{ __('Nhân viên') }}</th>
									<th class="p-3 border-b font-medium text-ink-gray-5 whitespace-nowrap">{{ __('Mã NV') }}</th>
									<th class="p-3 border-b font-medium text-ink-gray-5">{{ __('Khóa học') }}</th>
									<th class="p-3 border-b font-medium text-ink-gray-5 text-right">{{ __('Tiến độ') }}</th>
								</tr>
							</thead>
							<tbody>
								<tr v-for="user in dashboardStats.data.incomplete_users" class="hover:bg-surface-gray-2">
									<td class="p-3 border-b text-ink-gray-9">
										<router-link :to="{ name: 'Profile', params: { username: user.member } }" class="hover:underline">
											{{ user.full_name }}
										</router-link>
									</td>
									<td class="p-3 border-b text-ink-gray-7">{{ user.employee_code || '-' }}</td>
									<td class="p-3 border-b text-ink-gray-7">{{ user.course_title }}</td>
									<td class="p-3 border-b text-ink-gray-7 text-right">{{ user.progress }}%</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>

				<!-- Overdue Users -->
				<div class="border rounded-md overflow-hidden bg-surface-white shadow-sm">
					<div class="bg-surface-gray-2 px-4 py-3 border-b text-ink-red-6 font-semibold flex items-center gap-2">
						<span class="lucide-alert-triangle size-4" />
						{{ __('Nhân Sự Quá Hạn') }}
					</div>
					<div class="p-4" v-if="dashboardStats.data.overdue_users.length === 0">
						<div class="text-ink-gray-5 text-sm">{{ __('Không có nhân sự quá hạn.') }}</div>
					</div>
					<div class="max-h-96 overflow-y-auto" v-else>
						<table class="w-full text-left border-collapse text-sm">
							<thead class="bg-surface-gray-1 sticky top-0 z-10">
								<tr>
									<th class="p-3 border-b font-medium text-ink-gray-5 whitespace-nowrap">{{ __('Nhân viên') }}</th>
									<th class="p-3 border-b font-medium text-ink-gray-5">{{ __('Lớp/Batch') }}</th>
									<th class="p-3 border-b font-medium text-ink-gray-5">{{ __('Khóa học') }}</th>
									<th class="p-3 border-b font-medium text-ink-gray-5 text-right">{{ __('Tiến độ') }}</th>
								</tr>
							</thead>
							<tbody>
								<tr v-for="user in dashboardStats.data.overdue_users" class="hover:bg-surface-gray-2">
									<td class="p-3 border-b text-ink-gray-9">
										<router-link :to="{ name: 'Profile', params: { username: user.member } }" class="hover:underline">
											{{ user.full_name }}
										</router-link>
									</td>
									<td class="p-3 border-b text-ink-gray-7">{{ user.batch }}</td>
									<td class="p-3 border-b text-ink-gray-7">{{ user.course_title }}</td>
									<td class="p-3 border-b text-ink-red-6 font-medium text-right">{{ user.progress }}%</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { Button, LoadingIndicator, createResource, usePageMeta } from 'frappe-ui'
import { sessionStore } from '@/stores/session'

const { brand } = sessionStore()
const selectedCourse = ref('')

usePageMeta(() => ({
	title: __('Dashboard Quản Lý Đơn Vị'),
	icon: brand.favicon,
}))

const dashboardStats = createResource({
	url: 'lms.lms.api.get_unit_manager_dashboard',
	params: {
		course: selectedCourse.value
	},
	auto: true,
})

const courses = createResource({
	url: 'frappe.client.get_list',
	params: {
		doctype: 'LMS Course',
		fields: '["name", "title"]',
		limit_page_length: 500
	},
	auto: true
})

watch(selectedCourse, () => {
	dashboardStats.update({
		params: {
			course: selectedCourse.value
		}
	})
	dashboardStats.reload()
})

const exportReport = () => {
	if (!dashboardStats.data) return
	
	const incomplete = dashboardStats.data.incomplete_users
	const overdue = dashboardStats.data.overdue_users
	
	if (incomplete.length === 0 && overdue.length === 0) {
		alert(__('Không có dữ liệu để export'))
		return
	}
	
	const headers = ['Trạng thái', 'Nhân viên', 'Mã NV', 'Đơn vị', 'Khóa học', 'Tiến độ (%)']
	const csvRows = [headers.join(',')]
	
	for (const row of overdue) {
		const values = [
			`"Quá hạn"`,
			`"${row.full_name}"`,
			`"${row.employee_code || ''}"`,
			`"${row.department || ''}"`,
			`"${row.course_title}"`,
			row.progress
		]
		csvRows.push(values.join(','))
	}
	
	for (const row of incomplete) {
		const values = [
			`"Chưa hoàn thành"`,
			`"${row.full_name}"`,
			`"${row.employee_code || ''}"`,
			`"${row.department || ''}"`,
			`"${row.course_title}"`,
			row.progress
		]
		csvRows.push(values.join(','))
	}
	
	const csvString = '\uFEFF' + csvRows.join('\n') // Adding BOM for UTF-8 Excel support
	const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' })
	const url = URL.createObjectURL(blob)
	const a = document.createElement('a')
	a.href = url
	a.download = `baocao_daotao_donvi_${new Date().toISOString().split('T')[0]}.csv`
	document.body.appendChild(a)
	a.click()
	document.body.removeChild(a)
	URL.revokeObjectURL(url)
}
</script>
