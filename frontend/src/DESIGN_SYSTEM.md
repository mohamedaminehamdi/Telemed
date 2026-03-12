# Design System & Component Library

## Overview

Telemed design system provides a consistent, accessible, and modern UI framework for building healthcare applications.

## Colors

### Primary Colors
- **Primary Gradient**: #667eea → #764ba2 (Purple blend)
- **Primary**: #667eea
- **Dark Primary**: #5568d3

### Semantic Colors
- **Success**: #4caf50
- **Danger**: #ff6b6b / #ee5a6f
- **Warning**: #ffa500 / #ff9800
- **Info**: #2196f3

### Neutral Colors
- **White**: #ffffff
- **Light Gray**: #f9f9f9
- **Gray**: #f5f5f5
- **Dark Gray**: #999999
- **Text**: #333333

## Typography

### Font Family
- Body: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell
- Monospace: 'Monaco', 'Courier New'

### Font Sizes
- H1: 32px, 700 weight
- H2: 28px, 700 weight
- H3: 20px, 700 weight
- H4: 18px, 600 weight
- Body: 14px, 400 weight
- Small: 12px, 400 weight
- Caption: 11px, 500 weight

## Spacing

- xs: 4px
- sm: 8px
- md: 12px
- lg: 16px
- xl: 20px
- 2xl: 24px
- 3xl: 32px

## Components

### Button

```vue
<Button variant="primary" size="md" :loading="isLoading">
  Click Me
</Button>

<Button variant="secondary" icon="📝">
  Edit
</Button>

<Button variant="danger" disabled>
  Delete
</Button>
```

**Props:**
- `variant`: primary, secondary, danger, success, warning
- `size`: sm, md, lg
- `icon`: Icon emoji or string
- `loading`: Show loading spinner
- `disabled`: Disable button

### Card

```vue
<Card title="My Card">
  <p>Card content goes here</p>
  <template #footer>
    <div class="footer-content">Footer</div>
  </template>
</Card>
```

**Props:**
- `title`: Card title
- `elevated`: Add elevation shadow
- `clickable`: Add hover effect

**Slots:**
- `default`: Card body content
- `header`: Custom header content
- `footer`: Card footer content

### Modal

```vue
<Modal v-model="showModal" title="Confirm Action" size="md">
  <p>Are you sure you want to proceed?</p>
  <template #footer>
    <Button variant="primary" @click="confirm">Yes</Button>
    <Button variant="secondary" @click="showModal = false">No</Button>
  </template>
</Modal>
```

**Props:**
- `modelValue`: Show/hide modal
- `title`: Modal title
- `size`: sm, md, lg, xl

**Slots:**
- `default`: Modal body
- `footer`: Modal footer

## Layout

### Container
Max width: 1200px
Padding: 20px responsive

### Grid System
12-column responsive grid

### Breakpoints
- Mobile: < 640px
- Tablet: 640px - 1024px
- Desktop: > 1024px

## Shadows

- Subtle: 0 2px 8px rgba(0, 0, 0, 0.1)
- Medium: 0 4px 16px rgba(0, 0, 0, 0.15)
- Large: 0 20px 60px rgba(0, 0, 0, 0.3)

## Border Radius

- Small: 4px
- Default: 6px
- Medium: 8px
- Large: 12px

## Transitions

- Default: all 0.3s ease
- Fast: all 0.1s ease
- Slow: all 0.5s ease

## Accessibility

All components follow WCAG 2.1 guidelines:
- Proper color contrast (4.5:1 for text)
- Keyboard navigation support
- ARIA labels on interactive elements
- Focus indicators on all focusable elements
- Semantic HTML structure

## Best Practices

1. **Consistency**: Always use design system components
2. **Spacing**: Use predefined spacing scale
3. **Colors**: Only use defined color palette
4. **Typography**: Stick to typography scale
5. **Responsive**: Mobile-first responsive design
6. **States**: Always define hover, active, disabled states
7. **Feedback**: Provide visual feedback for user actions

## Theming

Customize colors by modifying CSS variables in your app:

```css
:root {
  --color-primary: #667eea;
  --color-danger: #ff6b6b;
  --color-success: #4caf50;
}
```

## Icons

Use emoji icons for simplicity:
- 📋 Document
- ✏️ Edit
- 🗑️ Delete
- ✅ Success
- ❌ Error
- ⚠️ Warning
- ℹ️ Info
- 🔒 Lock
- 👤 User
- 📱 Mobile
- 💻 Computer

## Animation

### Transitions
- Hover states: 0.3s ease
- Modal open/close: 0.3s ease
- Loading spinner: 0.6s linear infinite

### Transforms
- Hover up: translateY(-2px)
- Scale on click: scale(0.98)

## Form Components

### Input
- Height: 40px
- Padding: 10px 12px
- Border: 1px solid #e0e0e0
- Focus: Border #667eea + shadow

### Select
- Same as input
- Dropdown arrow on right

### Textarea
- Min height: 100px
- Resizable vertically

### Checkbox/Radio
- Size: 18px
- Spacing: 8px gap from label

## Dark Mode

Support planned: Use CSS system color scheme media query

## Version

Current: 1.0
Last Updated: 2026-03-12
