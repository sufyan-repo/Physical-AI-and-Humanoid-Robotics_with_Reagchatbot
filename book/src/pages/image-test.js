import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';

export default function ImageTest() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout title={`Image Test`} description="Test page for Robot.png">
      <div className="container padding-top--md padding-bottom--lg">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <h1>Robot Image Test</h1>
            <p>This page tests if the Robot.png image loads correctly.</p>
            <div style={{ textAlign: 'center', margin: '20px 0' }}>
              <img
                src="/img/Robot.png"
                alt="Robot Test"
                style={{ width: '200px', height: '200px', border: '1px solid #ccc' }}
              />
            </div>
            <p>If you see the robot image above, the path is correct.</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}