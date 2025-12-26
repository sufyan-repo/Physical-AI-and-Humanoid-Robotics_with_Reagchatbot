/**
 * Creating a sidebar enables you to:
 - Create an ordered group of docs
 - Render a sidebar in the docs portal

 - Learn more about Docusaurus sidebars: https://docusaurus.io/docs/sidebar
*/

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Foundations of Physical AI',
      link: {
        type: 'generated-index',
        title: 'Foundations of Physical AI',
        description: 'Explore the fundamental concepts of physical AI and embodied intelligence.',
        slug: '/category/foundations',
      },
      items: [
        'module1/introduction',
        'module1/basic_ai_concepts',
        'module1/embodied_intelligence',
        'module1/robot_hardware_overview',
      ],
    },
    {
      type: 'category',
      label: 'Humanoid Robotics Engineering',
      link: {
        type: 'generated-index',
        title: 'Humanoid Robotics Engineering',
        description: 'Delve into the engineering principles of humanoid robot design and control.',
        slug: '/category/robotics-engineering',
      },
      items: [
        'module2/humanoid_design_principles',
        'module2/kinematics_dynamics',
        'module2/locomotion_balance',
        'module2/actuator_control',
      ],
    },
    {
      type: 'category',
      label: 'Intelligence, Learning & Interaction',
      link: {
        type: 'generated-index',
        title: 'Intelligence, Learning & Interaction',
        description: 'Explore AI for robotic learning, decision-making, and human-robot interaction.',
        slug: '/category/intelligence-learning',
      },
      items: [
        'module3/robot_learning_paradigms',
        'module3/decision_making_planning',
        'module3/human_robot_interaction',
        'module3/social_ethical_implications',
      ],
    },
    {
      type: 'category',
      label: 'Applications, Future & Innovation',
      link: {
        type: 'generated-index',
        title: 'Applications, Future & Innovation',
        description: 'Discover real-world applications, emerging trends, and future directions in physical AI and robotics.',
        slug: '/category/applications-future',
      },
      items: [
        'module4/real_world_applications',
        'module4/emerging_trends',
        'module4/future_challenges',
        'module4/societal_impact_ethics',
      ],
    },
  ],
};

module.exports = sidebars;