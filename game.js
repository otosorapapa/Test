const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');

const keys = {};
window.addEventListener('keydown', e => keys[e.key.toLowerCase()] = true);
window.addEventListener('keyup', e => keys[e.key.toLowerCase()] = false);

const player = {
  x: canvas.width / 2,
  y: canvas.height - 50,
  size: 5,
  speed: 4,
  bullets: [],
  fireCooldown: 0
};

const enemy = {
  x: canvas.width / 2,
  y: 100,
  bullets: [],
  fireCooldown: 0
};

function spawnPlayerBullet() {
  player.bullets.push({ x: player.x, y: player.y, dy: -6 });
}

function spawnEnemyPattern() {
  const bulletSpeed = 2;
  for (let i = 0; i < 360; i += 15) {
    const angle = i * Math.PI / 180;
    enemy.bullets.push({
      x: enemy.x,
      y: enemy.y,
      dx: Math.cos(angle) * bulletSpeed,
      dy: Math.sin(angle) * bulletSpeed
    });
  }
}

function update() {
  // Player movement
  if (keys['arrowleft'] || keys['a']) player.x -= player.speed;
  if (keys['arrowright'] || keys['d']) player.x += player.speed;
  if (keys['arrowup'] || keys['w']) player.y -= player.speed;
  if (keys['arrowdown'] || keys['s']) player.y += player.speed;

  player.x = Math.max(0, Math.min(canvas.width, player.x));
  player.y = Math.max(0, Math.min(canvas.height, player.y));

  // Player shooting
  if ((keys['z'] || keys[' ']) && player.fireCooldown <= 0) {
    spawnPlayerBullet();
    player.fireCooldown = 10;
  }
  if (player.fireCooldown > 0) player.fireCooldown--;

  // Enemy shooting
  if (enemy.fireCooldown <= 0) {
    spawnEnemyPattern();
    enemy.fireCooldown = 60;
  } else {
    enemy.fireCooldown--;
  }

  // Update bullets
  player.bullets = player.bullets.filter(b => b.y > -10);
  player.bullets.forEach(b => b.y += b.dy);

  enemy.bullets = enemy.bullets.filter(b => b.x > -10 && b.x < canvas.width + 10 && b.y > -10 && b.y < canvas.height + 10);
  enemy.bullets.forEach(b => {
    b.x += b.dx;
    b.y += b.dy;
    // collision
    const dx = b.x - player.x;
    const dy = b.y - player.y;
    if (dx*dx + dy*dy < player.size * player.size) {
      alert('Game Over');
      window.location.reload();
    }
  });
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Draw player
  ctx.fillStyle = '#0f0';
  ctx.beginPath();
  ctx.arc(player.x, player.y, player.size, 0, Math.PI * 2);
  ctx.fill();

  // Draw player bullets
  ctx.fillStyle = '#ff0';
  player.bullets.forEach(b => {
    ctx.beginPath();
    ctx.arc(b.x, b.y, 3, 0, Math.PI * 2);
    ctx.fill();
  });

  // Draw enemy
  ctx.fillStyle = '#f00';
  ctx.beginPath();
  ctx.arc(enemy.x, enemy.y, 10, 0, Math.PI * 2);
  ctx.fill();

  // Draw enemy bullets
  ctx.fillStyle = '#0ff';
  enemy.bullets.forEach(b => {
    ctx.beginPath();
    ctx.arc(b.x, b.y, 4, 0, Math.PI * 2);
    ctx.fill();
  });
}

function loop() {
  update();
  draw();
  requestAnimationFrame(loop);
}

loop();
