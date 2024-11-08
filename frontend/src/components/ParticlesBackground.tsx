import React from 'react';
import { useCallback } from "react";
import type { Container, Engine } from "tsparticles-engine";
import Particles from "react-tsparticles";
import { loadSlim } from "tsparticles-slim";

interface ParticlesBackgroundProps {
  isDark: boolean;
}

const ParticlesBackground: React.FC<ParticlesBackgroundProps> = ({ isDark }) => {
  const particlesInit = useCallback(async (engine: Engine) => {
    await loadSlim(engine);
  }, []);

  return (
    <Particles
      id="tsparticles"
      init={particlesInit}
      className="fixed inset-0 -z-10 pointer-events-none"
      options={{
        background: {
          opacity: 0,
        },
        particles: {
          color: {
            value: isDark ? "#00FFF0" : "#BD00FF",
          },
          links: {
            color: isDark ? "#00FFF0" : "#BD00FF",
            distance: 150,
            enable: true,
            opacity: 0.2,
          },
          move: {
            enable: true,
            speed: 1,
          },
          number: {
            value: 30,
            density: {
              enable: true,
              value_area: 800,
            },
          },
          opacity: {
            value: 0.3,
          },
          shape: {
            type: "circle",
          },
          size: {
            value: { min: 1, max: 3 },
          },
        },
      }}
    />
  );
};

export default ParticlesBackground; 