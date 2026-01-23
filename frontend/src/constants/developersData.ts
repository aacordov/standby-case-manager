import { DeveloperProfile } from '../types/developer';

export const DEVELOPERS: DeveloperProfile[] = [
    {
        id: '1',
        name: 'Ronny Ortiz',
        role: 'Full Stack Developer',
        bio: 'Apasionado por crear experiencias web increíbles y escalables.',
        avatarUrl: '/images/team/ronny_ortiz.jpg',
        socialLinks: [
            { platform: 'github', url: 'https://github.com' },
            { platform: 'linkedin', url: 'https://linkedin.com' }
        ]
    },
    {
        id: '2',
        name: 'Allan Cordova',
        role: 'DevOps Engineer',
        bio: 'Especialista en Openshift automatización con Ansible y Sistemas Operativos.',
        avatarUrl: '/images/team/allan_cordova.jpg',
        socialLinks: [
            { platform: 'github', url: 'https://github.com' },
            { platform: 'twitter', url: 'https://twitter.com' }
        ]
    },
    {
        id: '3',
        name: 'Jose Briones',
        role: 'DevOps Engineer',
        bio: 'Especialista en arquitecturas robustas y optimización de bases de datos.',
        avatarUrl: '/images/team/jose_briones.jpg',
        socialLinks: [
            { platform: 'github', url: 'https://github.com' },
            { platform: 'linkedin', url: 'https://linkedin.com' }
        ]
    },
    {
        id: '4',
        name: 'Larry Sanchez',
        role: 'DevOps Engineer',
        bio: 'Automatizando todo lo que se mueve. Fanático de Docker y CI/CD.',
        avatarUrl: '/images/team/larry_sanchez.jpg',
        socialLinks: [
            { platform: 'github', url: 'https://github.com' },
            { platform: 'website', url: 'https://example.com' }
        ]
    }
];