import ModelViewer from '@metamask/logo';

const viewer = ModelViewer({
  pxNotRatio: true,
  width: 500,
  height: 400,
  followMouse: false,
  slowDrift: false,
});

const container = document.getElementById('logo-container');
container.appendChild(viewer.container);

viewer.lookAt({
  x: 100,
  y: 100,
});

viewer.setFollowMouse(true);

// To stop animation if needed
// viewer.stopAnimation();
