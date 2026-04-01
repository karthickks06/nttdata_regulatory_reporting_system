# shadcn/ui Components Installation

The shadcn/ui components need to be installed using the CLI tool. Run these commands:

```bash
cd frontend

# Install individual components as needed:
npx shadcn-ui@latest add button
npx shadcn-ui@latest add card
npx shadcn-ui@latest add dialog
npx shadcn-ui@latest add input
npx shadcn-ui@latest add label
npx shadcn-ui@latest add select
npx shadcn-ui@latest add table
npx shadcn-ui@latest add tabs
npx shadcn-ui@latest add form
npx shadcn-ui@latest add toast
npx shadcn-ui@latest add dropdown-menu
npx shadcn-ui@latest add badge
npx shadcn-ui@latest add alert
npx shadcn-ui@latest add sheet
npx shadcn-ui@latest add separator
npx shadcn-ui@latest add scroll-area
npx shadcn-ui@latest add skeleton

# Or install all at once:
npx shadcn-ui@latest add button card dialog input label select table tabs form toast dropdown-menu badge alert sheet separator scroll-area skeleton
```

These components will be automatically created in `src/components/ui/` directory.

**Note:** shadcn/ui components are meant to be installed via CLI, not manually created, as they have specific dependencies and configurations.
