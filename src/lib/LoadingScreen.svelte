<script>
  import { createEventDispatcher, onMount } from 'svelte';

  const dispatch = createEventDispatcher();
  let isExiting = false;

  onMount(() => {
    // Total animation time is roughly 3.5 seconds
    // After 3.5s we start the exit animation (fade out / scale down)
    const exitTimer = setTimeout(() => {
      isExiting = true;
    }, 4000);

    // After the exit animation finishes (e.g. 700ms), we remove the component
    const removeTimer = setTimeout(() => {
      dispatch('complete');
    }, 4700);

    return () => {
      clearTimeout(exitTimer);
      clearTimeout(removeTimer);
    };
  });
</script>

<div class="loading-screen {isExiting ? 'exiting' : ''}">
  <div class="intro-text">
    <span>A new partner</span><br/>
    <span class="indent">in your creative journey</span>
  </div>

  <div class="reveal-container">
    <svg class="reveal-svg" viewBox="0 0 800 200" preserveAspectRatio="xMidYMid meet">
      <defs>
        <!-- The clip path defines the "window" through which the logo is seen.
             We animate the rectangles inside it to slide across. -->
        <clipPath id="bars-clip">
          <!-- Colorful bars sliding from left to right -->
          <!-- They will be animated via CSS. We start them off-screen (e.g. x="-1000") -->
          <rect class="bar bar-1" y="0" height="200" width="100" />
          <rect class="bar bar-2" y="0" height="200" width="150" />
          <rect class="bar bar-3" y="0" height="200" width="80" />
          <rect class="bar bar-4" y="0" height="200" width="600" />
        </clipPath>
      </defs>

      <!-- The colorful bars themselves that visually slide across the screen.
           We use the exact same animation so they sync perfectly with the clip path. -->
      <g class="visual-bars">
        <rect class="bar bar-1" fill="#fff" y="0" height="200" width="100" />
        <rect class="bar bar-2" fill="#ff4d85" y="0" height="200" width="150" />
        <rect class="bar bar-3" fill="#00e5ff" y="0" height="200" width="80" />
        <rect class="bar bar-4" fill="#304ffe" y="0" height="200" width="600" />
      </g>

      <!-- The Vybe Central Logo text, revealed by the clip path -->
      <text 
        x="50%" 
        y="55%" 
        text-anchor="middle" 
        dominant-baseline="middle" 
        class="logo-text"
        clip-path="url(#bars-clip)"
      >
        VYBE CENTRAL
      </text>
    </svg>
  </div>
</div>

<style>
  .loading-screen {
    position: fixed;
    inset: 0;
    z-index: 9999;
    background-color: #000;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    overflow: hidden;
    transition: transform 0.7s cubic-bezier(0.76, 0, 0.24, 1), 
                opacity 0.7s cubic-bezier(0.76, 0, 0.24, 1);
  }

  .loading-screen.exiting {
    transform: scale(0.9);
    opacity: 0;
    pointer-events: none;
  }

  /* Introductory text */
  .intro-text {
    position: absolute;
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: clamp(1.5rem, 4vw, 3rem);
    font-weight: 400;
    line-height: 1.2;
    letter-spacing: -0.02em;
    opacity: 0;
    animation: fadeIntro 2s forwards;
    z-index: 1;
  }

  .intro-text .indent {
    margin-left: 2em;
  }

  @keyframes fadeIntro {
    0% { opacity: 0; transform: translateY(10px); }
    10% { opacity: 1; transform: translateY(0); }
    70% { opacity: 1; transform: translateY(0); }
    80% { opacity: 0; transform: translateY(-10px); }
    100% { opacity: 0; }
  }

  /* Reveal Container */
  .reveal-container {
    position: absolute;
    width: 100%;
    max-width: 1200px;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
  }

  .reveal-svg {
    width: 100%;
    height: 100%;
  }

  .logo-text {
    font-family: "Plus Jakarta Sans", sans-serif;
    font-weight: 800;
    font-size: 80px;
    fill: #fff;
    letter-spacing: -0.03em;
  }

  /* SVG Bars Animation */
  .bar {
    x: -800; /* Start completely off screen left */
    /* Note: x attribute is animated via CSS */
  }

  /* Using CSS to animate SVG attributes isn't perfectly supported in all older browsers,
     but animating transform: translateX is robust. We will use transform. */
  .bar {
    transform: translateX(-1200px);
    animation: slideAcross 2.5s cubic-bezier(0.76, 0, 0.24, 1) forwards;
  }

  /* We stagger the bars to create a layered sliding effect */
  .bar-1 { animation-delay: 0.8s; }
  .bar-2 { animation-delay: 0.9s; }
  .bar-3 { animation-delay: 0.95s; }
  .bar-4 { animation-delay: 1.05s; }

  @keyframes slideAcross {
    0% { transform: translateX(-1200px); }
    100% { transform: translateX(1800px); }
  }
</style>
