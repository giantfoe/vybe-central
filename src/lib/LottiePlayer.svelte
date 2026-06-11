<script>
  import { onMount } from 'svelte';
  import lottie from 'lottie-web';

  export let animationData;
  export let loop = true;
  export let autoplay = true;
  export let renderer = 'svg';
  export let ariaLabel = 'Animated graphic';

  let container;

  onMount(() => {
    const animation = lottie.loadAnimation({
      container,
      renderer,
      loop,
      autoplay,
      animationData
    });

    return () => animation.destroy();
  });
</script>

<div class="lottie-frame" bind:this={container} role="img" aria-label={ariaLabel}></div>

