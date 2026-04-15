<template>
  <Card class="mb-6">
    <template #header>
      <div class="flex items-center justify-between p-4 bg-primary/10 rounded-t-lg">
        <h3 class="text-lg font-semibold text-primary">PrimeVue Компоненты</h3>
        <Badge :value="9" severity="success" />
      </div>
    </template>
    <template #title>Демонстрация UI-компонентов</template>
    <template #content>
      <div class="space-y-4">
        <!-- Buttons -->
        <div class="flex flex-wrap gap-2">
          <Button label="Primary" />
          <Button label="Secondary" severity="secondary" />
          <Button label="Success" severity="success" />
          <Button label="Info" severity="info" />
          <Button label="Danger" severity="danger" />
        </div>

        <!-- Input Fields -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <InputText 
            v-model="inputValue" 
            placeholder="Текстовое поле" 
            class="w-full"
          />
          <InputNumber 
            v-model="numberValue" 
            placeholder="Числовое поле" 
            class="w-full"
          />
        </div>

        <!-- Dropdown -->
        <Dropdown 
          v-model="selectedCategory" 
          :options="categories" 
          option-label="name" 
          option-value="code"
          placeholder="Выберите категорию"
          class="w-full"
        />

        <!-- Toast Notification -->
        <Button 
          label="Показать уведомление" 
          severity="info" 
          @click="showToast"
        />

        <!-- Dialog Toggle -->
        <Button 
          :label="dialogVisible ? 'Закрыть диалог' : 'Открыть диалог'" 
          severity="secondary"
          @click="dialogVisible = !dialogVisible"
        />

        <!-- Dialog -->
        <Dialog 
          v-model:visible="dialogVisible" 
          modal 
          header="Пример диалога"
          :style="{ width: '30rem' }"
        >
          <div class="space-y-4">
            <p>Это пример диалогового окна с PrimeVue.</p>
            <InputText placeholder="Введите текст" class="w-full" />
          </div>
          <template #footer>
            <Button label="Отмена" severity="secondary" @click="dialogVisible = false" />
            <Button label="OK" @click="dialogVisible = false" />
          </template>
        </Dialog>

        <!-- Progress Spinner -->
        <div class="flex items-center gap-4">
          <ProgressSpinner v-if="loading" style="width: 50px" />
          <Button 
            :label="loading ? 'Загрузка...' : 'Запустить'" 
            :disabled="loading"
            @click="startLoading"
          />
        </div>

        <!-- Table Example -->
        <DataTable 
          :value="recipes" 
          tableStyle="min-width: 50rem"
          stripedRows
        >
          <Column field="title" header="Название" sortable></Column>
          <Column field="cuisine" header="Кухня" sortable></Column>
          <Column field="difficulty" header="Сложность">
            <template #body="slotProps">
              <Tag :value="slotProps.data.difficulty" :severity="getDifficultySeverity(slotProps.data.difficulty)" />
            </template>
          </Column>
          <Column header="Действия">
            <template #body>
              <Button icon="pi pi-pencil" severity="secondary" size="small" class="mr-2" />
              <Button icon="pi pi-trash" severity="danger" size="small" />
            </template>
          </Column>
        </DataTable>

        <!-- Tabs -->
        <TabView>
          <TabPanel header="Ингредиенты">
            <p>Список ингредиентов...</p>
          </TabPanel>
          <TabPanel header="Шаги">
            <p>Шаги приготовления...</p>
          </TabPanel>
          <TabPanel header="Заметки">
            <p>Дополнительные заметки...</p>
          </TabPanel>
        </TabView>
      </div>
    </template>
  </Card>
</template>

<script setup>
import { ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Card from 'primevue/card'
import InputText from 'primevue/inputtext'
import InputNumber from 'primevue/inputnumber'
import Dropdown from 'primevue/dropdown'
import Dialog from 'primevue/dialog'
import ProgressSpinner from 'primevue/progressspinner'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Tag from 'primevue/tag'
import TabView from 'primevue/tabview'
import TabPanel from 'primevue/tabpanel'
import Badge from 'primevue/badge'

const inputValue = ref('')
const numberValue = ref(null)
const selectedCategory = ref(null)
const dialogVisible = ref(false)
const loading = ref(false)

const toast = useToast()

const categories = ref([
  { name: 'Все категории', code: 'all' },
  { name: 'Завтрак', code: 'breakfast' },
  { name: 'Обед', code: 'lunch' },
  { name: 'Ужин', code: 'dinner' },
  { name: 'Десерт', code: 'dessert' }
])

const recipes = ref([
  { title: 'Паста Карбонара', cuisine: 'Итальянская', difficulty: 'Средняя' },
  { title: 'Борщ', cuisine: 'Украинская', difficulty: 'Сложная' },
  { title: 'Салат Цезарь', cuisine: 'Американская', difficulty: 'Легкая' }
])

const showToast = () => {
  toast.add({
    severity: 'success',
    summary: 'Успешно',
    detail: 'Операция выполнена успешно',
    life: 3000
  })
}

const startLoading = () => {
  loading.value = true
  setTimeout(() => {
    loading.value = false
    showToast()
  }, 2000)
}

const getDifficultySeverity = (difficulty) => {
  const map = {
    'Легкая': 'success',
    'Средняя': 'warning',
    'Сложная': 'danger'
  }
  return map[difficulty] || 'secondary'
}
</script>
