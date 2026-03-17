/**
 * Frontend Tests - Vue Component Tests
 * Using Vitest + Vue Test Utils
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import Button from '@/components/shared/Button.vue'
import Card from '@/components/shared/Card.vue'
import Modal from '@/components/shared/Modal.vue'
import AppointmentCard from '@/components/AppointmentCard.vue'


describe('Button Component', () => {
  it('renders button with text', () => {
    const wrapper = mount(Button, {
      slots: {
        default: 'Click Me'
      }
    })
    expect(wrapper.text()).toContain('Click Me')
  })

  it('applies variant classes', () => {
    const wrapper = mount(Button, {
      props: {
        variant: 'primary'
      },
      slots: {
        default: 'Button'
      }
    })
    expect(wrapper.classes()).toContain('btn-primary')
  })

  it('applies size classes', () => {
    const wrapper = mount(Button, {
      props: {
        size: 'lg'
      },
      slots: {
        default: 'Button'
      }
    })
    expect(wrapper.classes()).toContain('btn-lg')
  })

  it('disables button when disabled prop is true', () => {
    const wrapper = mount(Button, {
      props: {
        disabled: true
      },
      slots: {
        default: 'Button'
      }
    })
    expect(wrapper.find('button').attributes('disabled')).toBeDefined()
  })

  it('emits click event', async () => {
    const wrapper = mount(Button, {
      slots: {
        default: 'Click'
      }
    })
    await wrapper.find('button').trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })

  it('shows loading spinner when loading', () => {
    const wrapper = mount(Button, {
      props: {
        loading: true
      },
      slots: {
        default: 'Loading'
      }
    })
    expect(wrapper.find('.spinner').exists()).toBe(true)
  })
})


describe('Card Component', () => {
  it('renders card title', () => {
    const wrapper = mount(Card, {
      props: {
        title: 'Test Card'
      },
      slots: {
        default: 'Content'
      }
    })
    expect(wrapper.text()).toContain('Test Card')
  })

  it('renders slot content', () => {
    const wrapper = mount(Card, {
      slots: {
        default: 'Card content'
      }
    })
    expect(wrapper.text()).toContain('Card content')
  })

  it('renders header slot', () => {
    const wrapper = mount(Card, {
      slots: {
        header: 'Custom Header'
      }
    })
    expect(wrapper.find('.card-header').text()).toContain('Custom Header')
  })

  it('renders footer slot', () => {
    const wrapper = mount(Card, {
      slots: {
        footer: 'Card Footer'
      }
    })
    expect(wrapper.find('.card-footer').text()).toContain('Card Footer')
  })
})


describe('Modal Component', () => {
  it('shows modal when modelValue is true', () => {
    const wrapper = mount(Modal, {
      props: {
        modelValue: true,
        title: 'Test Modal'
      }
    })
    expect(wrapper.find('.modal-overlay').exists()).toBe(true)
  })

  it('hides modal when modelValue is false', () => {
    const wrapper = mount(Modal, {
      props: {
        modelValue: false
      }
    })
    expect(wrapper.find('.modal-overlay').exists()).toBe(false)
  })

  it('displays modal title', () => {
    const wrapper = mount(Modal, {
      props: {
        modelValue: true,
        title: 'Modal Title'
      }
    })
    expect(wrapper.text()).toContain('Modal Title')
  })

  it('emits update:modelValue when close button clicked', async () => {
    const wrapper = mount(Modal, {
      props: {
        modelValue: true
      }
    })
    await wrapper.find('.close-button').trigger('click')
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
  })

  it('applies size classes', () => {
    const wrapper = mount(Modal, {
      props: {
        modelValue: true,
        size: 'lg'
      }
    })
    expect(wrapper.find('.modal-dialog').classes()).toContain('modal-lg')
  })
})


describe('AppointmentCard Component', () => {
  const mockAppointment = {
    id: 1,
    doctor: {
      user: {
        full_name: 'Dr. Smith'
      },
      specialization: 'Cardiology'
    },
    scheduled_at: new Date().toISOString(),
    duration_minutes: 30,
    status: 'confirmed',
    reason: 'Heart checkup'
  }

  it('displays doctor name', () => {
    const wrapper = mount(AppointmentCard, {
      props: {
        appointment: mockAppointment
      }
    })
    expect(wrapper.text()).toContain('Dr. Smith')
  })

  it('displays appointment status', () => {
    const wrapper = mount(AppointmentCard, {
      props: {
        appointment: mockAppointment
      }
    })
    expect(wrapper.text()).toContain('confirmed')
  })

  it('emits confirm event', async () => {
    const wrapper = mount(AppointmentCard, {
      props: {
        appointment: mockAppointment
      }
    })
    const confirmButton = wrapper.findAll('button').find(btn =>
      btn.text().includes('Confirm')
    )
    if (confirmButton) {
      await confirmButton.trigger('click')
      expect(wrapper.emitted('confirm')).toBeTruthy()
    }
  })

  it('displays duration', () => {
    const wrapper = mount(AppointmentCard, {
      props: {
        appointment: mockAppointment
      }
    })
    expect(wrapper.text()).toContain('30')
  })
})


describe('Integration Tests', () => {
  it('button in modal works correctly', async () => {
    const wrapper = mount({
      template: `
        <Modal v-model="showModal">
          <Button @click="handleClick">Click Me</Button>
        </Modal>
      `,
      components: { Modal, Button },
      data() {
        return { showModal: true }
      },
      methods: {
        handleClick() {
          this.clicked = true
        }
      }
    })

    const button = wrapper.find('button')
    await button.trigger('click')
    expect(wrapper.vm.clicked).toBe(true)
  })

  it('card in modal displays content', () => {
    const wrapper = mount({
      template: `
        <Modal v-model="showModal">
          <Card title="Test">Content</Card>
        </Modal>
      `,
      components: { Modal, Card },
      data() {
        return { showModal: true }
      }
    })

    expect(wrapper.text()).toContain('Test')
    expect(wrapper.text()).toContain('Content')
  })
})
