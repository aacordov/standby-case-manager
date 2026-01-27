import { DeveloperProfile } from '../types/developer';

export const DEVELOPERS: DeveloperProfile[] = [
    {
        id: '1',
        name: 'Ronny Ortiz',
        role: 'Full Stack Developer',
        bio: 'Apasionado por crear experiencias web increíbles y escalables.',
        avatarUrl: '/images/team/ronny_ortiz.jpg',
        socialLinks: [
            { platform: 'github', url: 'https://github.com/rortiz-09' },
            { platform: 'linkedin', url: 'https://www.linkedin.com/in/ronnyortiz/' }
        ]
    },
    {
        id: '2',
        name: 'Allan Cordova',
        role: 'DevOps Engineer',
        bio: 'Especialista en Openshift automatización con Ansible y Sistemas Operativos.',
        avatarUrl: '/images/team/allan_cordova.jpg',
        socialLinks: [
            { platform: 'github', url: 'https://github.com/aacordov' },
            { platform: 'linkedin', url: 'https://www.linkedin.com/in/allan-cordova-duque-211279147' }
        ]
    },
    {
        id: '3',
        name: 'Jose Briones',
        role: 'DevOps Engineer',
        bio: 'Especialista en arquitecturas robustas y optimización de bases de datos.',
        avatarUrl: '/images/team/jose_briones.jpg',
        socialLinks: [
            { platform: 'github', url: 'https://github.com/josmbrio' },
            { platform: 'linkedin', url: 'https://www.linkedin.com/in/josemabriones/' }
        ]
    },
    {
        id: '4',
        name: 'Larry Sanchez',
        role: 'DevOps Engineer',
        bio: 'Automatizando todo lo que se mueve. Fanático de Docker y CI/CD.',
        avatarUrl: '/images/team/larry_sanchez.jpg',
        socialLinks: [
            { platform: 'github', url: 'https://github.com/lsancheg' },
            { platform: 'linkedin', url: 'www.linkedin.com/in/lajasanc' }
        ]
    }
];