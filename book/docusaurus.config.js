// @ts-check
import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Intelligent Robotics in the Physical World',
  tagline: 'A Comprehensive Guide to Embodied Intelligence and Humanoid Robot Design',
  favicon: 'img/logo.png',

  // Enable future v4 features
  future: {
    v4: true,
  },

  // Hosting URL
  url: 'http://localhost:3000',
  baseUrl: '/',

  // GitHub info
  organizationName: 'M.sufyan',
  projectName: 'spect-kit-book',
  deploymentBranch: 'gh-pages',

  onBrokenLinks: 'warn',
  onBrokenMarkdownLinks: 'warn',
  markdown: {
    format: 'detect',
    mermaid: false,
    // Ignore broken image errors to allow development to continue
    hooks: {
      onBrokenMarkdownImages: 'ignore',
    },
  },

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig: {
    image: 'img/docusaurus-social-card.jpg',
    colorMode: {
      respectPrefersColorScheme: true,
    },

    navbar: {
      title: 'Intelligent Robotics in the Physical World',
      logo: {
        alt: 'Site Logo',
        src: 'img/logo.png',
      },
      items: [
        { type: 'docSidebar', sidebarId: 'tutorialSidebar', position: 'left', label: 'Book' },
        { to: '/login', label: 'Login', position: 'right' },
        { to: '/signup', label: 'Sign Up', position: 'right' },
        {
          href: 'https://github.com/sufyan-repo',
          label: 'GitHub',
          position: 'right',
        },
        { type: 'search', position: 'right' },
      ],
    },

    footer: {
      style: 'dark',
      links: [
        {
          title: 'About This Book',
          items: [
            { label: 'Introduction', to: '/docs/intro' },
            { label: 'Getting Started', to: '/docs/module1/introduction' },
          ],
        },
        {
          title: 'Quick Links',
          items: [
            { label: 'Home', to: '/' },
            { label: 'All Chapters', to: '/docs/intro' },
            { label: 'Search', to: '/search' },
          ],
        },
        {
          title: 'Connect',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/sufyan-repo',
            },
          ],
        },
      ],
      copyright: `
        <div style="text-align: center; padding-top: 10px;">
          <strong>© 2025 Muhammad Sufyan</strong> — All Rights Reserved.
          <br/>
          Built for learning & innovation in Intelligent Robotics in the Physical World.
        </div>
      `,
    },

    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  },
};

export default config;