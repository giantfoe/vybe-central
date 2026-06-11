<script>
  // Very high quality SVG Shader using fluid displacement maps and CSS gradients
</script>

<div class="fluid-shader-container">
  <div class="color-orbs">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="orb orb-4"></div>
  </div>

  <svg class="shader-defs">
    <defs>
      <filter id="liquid-filter" x="-20%" y="-20%" width="140%" height="140%">
        <!-- Animated fractal noise -->
        <feTurbulence 
          type="fractalNoise" 
          baseFrequency="0.0015" 
          numOctaves="3" 
          result="noise"
        >
          <animate 
            attributeName="baseFrequency" 
            values="0.0015; 0.003; 0.0015" 
            dur="20s" 
            repeatCount="indefinite"
          />
        </feTurbulence>
        
        <!-- Displace the underlying color orbs using the noise -->
        <feDisplacementMap 
          in="SourceGraphic" 
          in2="noise" 
          scale="250" 
          xChannelSelector="R" 
          yChannelSelector="G" 
          result="displaced"
        />
        
        <!-- Increase contrast for a more vibrant, high-end look -->
        <feColorMatrix type="matrix" values="
          1 0 0 0 0
          0 1 0 0 0
          0 0 1 0 0
          0 0 0 20 -5" 
          in="displaced"
          result="high-contrast"
        />
        
        <feBlend in="high-contrast" in2="SourceGraphic" mode="screen" />
      </filter>
      
      <!-- Optional static grain overlay -->
      <filter id="grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" stitchTiles="stitch" />
      </filter>
    </defs>
  </svg>
  
  <div class="grain-overlay"></div>
</div>

<style>
  .fluid-shader-container {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    background-color: #05050a; /* Deep cinematic dark base */
    overflow: hidden;
    z-index: 0;
  }

  .color-orbs {
    position: absolute;
    inset: -20%;
    width: 140%;
    height: 140%;
    /* Apply the SVG displacement filter to the orbs to create the fluid effect */
    filter: url(#liquid-filter);
    opacity: 0.85;
  }

  .orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    mix-blend-mode: screen;
    animation: float-orb 25s infinite ease-in-out alternate;
  }

  .orb-1 {
    top: 20%;
    left: 10%;
    width: 60vw;
    height: 60vw;
    background: #3b82f6; /* Blue */
  }

  .orb-2 {
    bottom: 10%;
    right: 10%;
    width: 70vw;
    height: 70vw;
    background: #ec4899; /* Pink */
    animation-delay: -5s;
    animation-duration: 20s;
  }

  .orb-3 {
    top: 30%;
    left: 50%;
    width: 50vw;
    height: 50vw;
    background: #8b5cf6; /* Purple */
    animation-delay: -10s;
  }

  .orb-4 {
    bottom: 30%;
    left: 20%;
    width: 40vw;
    height: 40vw;
    background: #0ea5e9; /* Light blue */
    animation-delay: -15s;
    animation-duration: 30s;
  }

  @keyframes float-orb {
    0% { transform: translate(0, 0) scale(1) rotate(0deg); }
    33% { transform: translate(15vw, 10vh) scale(1.1) rotate(10deg); }
    66% { transform: translate(-10vw, -15vh) scale(0.9) rotate(-10deg); }
    100% { transform: translate(5vw, 5vh) scale(1) rotate(0deg); }
  }

  .shader-defs {
    position: absolute;
    width: 0;
    height: 0;
    pointer-events: none;
  }

  .grain-overlay {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 2;
    opacity: 0.15;
    mix-blend-mode: overlay;
    background: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noiseFilter)'/%3E%3C/svg%3E");
  }
</style>
