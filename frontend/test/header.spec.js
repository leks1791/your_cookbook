import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Header from '../src/components/Header.vue'
import { useAuthStore } from '../src/stores/auth'
import { nextTick } from 'vue'

// Mock API to avoid real HTTP calls
import api from '../src/api'
vi.mock('../src/api', () => ({
  default: {
    get: vi.fn(() => Promise.resolve({ data: { username: 'Alex' } }))
  }
}))

describe('Header.vue', () => {
  let pinia
  beforeEach(() => {
    pinia = createPinia()
    setActivePinia(pinia)
  })

  test('does not show greeting when not authenticated', async () => {
    const wrapper = mount(Header, {
      global: {
        plugins: [pinia],
        stubs: { 'router-link': true },
      }
    })

    // Greeting text should not appear
    expect(wrapper.text()).not.toContain('Привет')
  })

  test('shows greeting when authenticated and updates after fetch', async () => {
    const store = useAuthStore()
    store.token = 'token123'
    // mount header after configuring store
    const wrapper = mount(Header, {
      global: {
        plugins: [pinia],
        stubs: { 'router-link': true },
      }
    })

    // simulate fetchMe populating username
    await store.fetchMe()
    await nextTick()
    expect(wrapper.text()).toContain('Привет,')
  })

  test('emits logout event when clicking logout button', async () => {
    const store = useAuthStore()
    store.token = 'token123'
    const wrapper = mount(Header, {
      global: {
        plugins: [pinia],
        stubs: { 'router-link': true },
      }
    })
    // click logout
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted()).toHaveProperty('logout')
  })
})
