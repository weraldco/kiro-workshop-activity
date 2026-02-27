/**
 * Seed script to populate the database with test workshops
 * Run with: npx ts-node src/seed-data.ts
 */

import { DatabaseService } from './services/database.service';
import { v4 as uuidv4 } from 'uuid';

const testWorkshops = [
  {
    id: uuidv4(),
    title: 'TypeScript Fundamentals',
    description: 'Learn the basics of TypeScript including types, interfaces, and generics',
    status: 'pending' as const,
    signup_enabled: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: uuidv4(),
    title: 'Advanced React Patterns',
    description: 'Master advanced React concepts like hooks, context, and performance optimization',
    status: 'ongoing' as const,
    signup_enabled: false,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: uuidv4(),
    title: 'Node.js Best Practices',
    description: 'Learn Node.js best practices for building scalable backend applications',
    status: 'completed' as const,
    signup_enabled: false,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: uuidv4(),
    title: 'Web Security Essentials',
    description: 'Understanding common web vulnerabilities and how to prevent them',
    status: 'pending' as const,
    signup_enabled: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
  {
    id: uuidv4(),
    title: 'GraphQL API Design',
    description: 'Build efficient and scalable GraphQL APIs with best practices',
    status: 'pending' as const,
    signup_enabled: true,
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  },
];

// Seed the database
try {
  DatabaseService.writeWorkshops(testWorkshops);
  console.log('✅ Successfully seeded database with test workshops');
  console.log(`📊 Added ${testWorkshops.length} workshops`);
  testWorkshops.forEach((workshop, index) => {
    console.log(`   ${index + 1}. ${workshop.title} (${workshop.status})`);
  });
} catch (error) {
  console.error('❌ Failed to seed database:', error);
  process.exit(1);
}
