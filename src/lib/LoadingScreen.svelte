<script>
  import { createEventDispatcher, onMount } from 'svelte';

  const dispatch = createEventDispatcher();
  let isExiting = false;

  onMount(() => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const exitDelay = reduceMotion ? 350 : 3200;
    const removeDelay = reduceMotion ? 450 : 3850;

    const exitTimer = setTimeout(() => {
      isExiting = true;
    }, exitDelay);

    const removeTimer = setTimeout(() => {
      dispatch('complete');
    }, removeDelay);

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

  <div class="reveal-container" aria-hidden="true">
    <div class="logo-reveal">
      <div class="logo-text">VYBE CENTRAL</div>
      <div class="bar bar-1"></div>
      <div class="bar bar-2"></div>
      <div class="bar bar-3"></div>
      <div class="bar bar-4"></div>
    </div>
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
    isolation: isolate;
    transition: transform 0.7s cubic-bezier(0.76, 0, 0.24, 1), 
                opacity 0.7s cubic-bezier(0.76, 0, 0.24, 1);
  }

  .loading-screen.exiting {
    transform: scale(0.96);
    opacity: 0;
    pointer-events: none;
  }

  .intro-text {
    position: absolute;
    width: min(88vw, 44rem);
    font-family: "Plus Jakarta Sans", sans-serif;
    font-size: clamp(1.5rem, 4vw, 3.1rem);
    font-weight: 400;
    line-height: 1.14;
    letter-spacing: 0;
    opacity: 0;
    animation: fadeIntro 1.7s forwards;
    z-index: 1;
  }

  .intro-text .indent {
    display: inline-block;
    margin-left: clamp(1.25rem, 7vw, 5.5rem);
  }

  @keyframes fadeIntro {
    0% { opacity: 0; transform: translateY(10px); }
    14% { opacity: 1; transform: translateY(0); }
    68% { opacity: 1; transform: translateY(0); }
    100% { opacity: 0; transform: translateY(-10px); }
  }

  @keyframes revealStage {
    0%, 100% { opacity: 1; }
  }

  @keyframes logoWipe {
    0% {
      opacity: 0;
      clip-path: inset(0 100% 0 0);
      transform: translateY(0.1em);
    }
    18% { opacity: 1; }
    100% {
      opacity: 1;
      clip-path: inset(0 0 0 0);
      transform: translateY(0);
    }
  }

  @keyframes slideAcross {
    0% { transform: translate3d(-120%, 0, 0); }
    100% { transform: translate3d(140%, 0, 0); }
  }

  @keyframes barFade {
    0%, 82% { opacity: 1; }
    100% { opacity: 0; }
  }

  .reveal-container {
    position: absolute;
    width: min(90vw, 58rem);
    height: clamp(5rem, 16vw, 10rem);
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    animation: revealStage 1.5s 1.72s forwards;
    z-index: 2;
  }

  .logo-reveal {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
    contain: layout paint style;
  }

  .logo-text {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: "Plus Jakarta Sans", sans-serif;
    font-weight: 800;
    font-size: clamp(2.35rem, 8.2vw, 5.6rem);
    line-height: 1;
    letter-spacing: 0;
    white-space: nowrap;
    opacity: 0;
    animation: logoWipe 1.05s 1.92s cubic-bezier(0.76, 0, 0.24, 1) forwards;
  }

  .bar {
    position: absolute;
    top: 0;
    bottom: 0;
    left: -22%;
    will-change: transform, opacity;
    transform: translate3d(-120%, 0, 0);
    animation: slideAcross 1.2s cubic-bezier(0.76, 0, 0.24, 1) forwards,
               barFade 1.2s linear forwards;
  }

  .bar-1 {
    width: 13%;
    background: #fff;
    animation-delay: 1.74s;
  }

  .bar-2 {
    width: 21%;
    background: #ff4d85;
    animation-delay: 1.82s;
  }

  .bar-3 {
    width: 12%;
    background: #00e5ff;
    animation-delay: 1.9s;
  }

  .bar-4 {
    width: 72%;
    background: #304ffe;
    animation-delay: 1.98s;
  }

  @media (max-width: 640px) {
    .intro-text {
      width: min(86vw, 24rem);
      font-size: clamp(1.35rem, 7vw, 2.35rem);
      line-height: 1.12;
    }

    .intro-text .indent {
      margin-left: clamp(0.75rem, 9vw, 2.5rem);
    }

    .reveal-container {
      width: min(88vw, 24rem);
      height: clamp(4.25rem, 22vw, 6.5rem);
    }

    .logo-text {
      font-size: clamp(2rem, 10vw, 3.25rem);
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .loading-screen,
    .intro-text,
    .reveal-container,
    .logo-text,
    .bar {
      animation-duration: 0.01ms !important;
      animation-delay: 0ms !important;
      transition-duration: 0.01ms !important;
    }

    .intro-text,
    .bar {
      display: none;
    }

    .reveal-container,
    .logo-text {
      opacity: 1;
      clip-path: none;
    }
  }
</style>
