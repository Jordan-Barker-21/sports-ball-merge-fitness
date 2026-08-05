"""
Ball Merge Fitness Game - SPORTS BALL EDITION! 🏀⚽🎾🏈⚾
Values map to different sports balls:
1 → Tennis Ball (🎾)
2 → Baseball (⚾)
4 → Golf Ball (🏌️)
8 → Soccer Ball (⚽)
16 → Basketball (🏀)
32 → Volleyball (🏐)
64 → American Football (🏈)
128 → Bowling Ball (🎳)
256 → Rugby Ball (🏉)
512 → Cricket Ball (🏏)
1024 → Beach Ball (🏖️)
2048 → Planet Earth 🌍 (because why not!)
"""

import cv2
import pygame
import sys
import math
import random
import time
import numpy as np
from collections import deque
import mediapipe as mp

# ============ CONFIGURATION ============
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
GAME_AREA_TOP = 150
GAME_AREA_BOTTOM = 600
BALL_RADIUS = 25  # Slightly bigger for sports ball detail
FALL_SPEED = 3
MERGE_THRESHOLD = 1.2
KNEE_FLEX_THRESHOLD = 80
SQUAT_HOLD_FRAMES = 10
SIDE_LUNGE_THRESHOLD = 0.15
TIMED_MODE_DURATION = 60

# ============ MEDIAPIPE SETUP ============
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# ============ SPORTS BALL RENDERER ============
class SportsBallRenderer:
    """Procedurally draw different sports balls"""
    
    @staticmethod
    def draw_tennis_ball(surface, x, y, radius):
        # Neon yellow-green with fuzzy texture
        pygame.draw.circle(surface, (200, 230, 50), (x, y), radius)
        # Fuzzy lines
        for i in range(0, 360, 15):
            angle = math.radians(i)
            start_x = x + radius * 0.6 * math.cos(angle)
            start_y = y + radius * 0.6 * math.sin(angle)
            end_x = x + radius * 0.9 * math.cos(angle)
            end_y = y + radius * 0.9 * math.sin(angle)
            pygame.draw.line(surface, (180, 210, 30), (start_x, start_y), (end_x, end_y), 1)
        # Seam lines
        pygame.draw.arc(surface, (150, 180, 20), (x-radius, y-radius, radius*2, radius*2), 
                        math.radians(30), math.radians(150), 2)
        pygame.draw.arc(surface, (150, 180, 20), (x-radius, y-radius, radius*2, radius*2), 
                        math.radians(210), math.radians(330), 2)
    
    @staticmethod
    def draw_baseball(surface, x, y, radius):
        # White with red stitching
        pygame.draw.circle(surface, (255, 255, 255), (x, y), radius)
        # Red stitching pattern (simplified)
        for offset in [-3, 3]:
            points = []
            for i in range(0, 360, 10):
                angle = math.radians(i)
                r = radius - 2 + offset * math.sin(angle * 2)
                px = x + r * math.cos(angle)
                py = y + r * math.sin(angle) * 0.7
                points.append((px, py))
            if len(points) > 2:
                pygame.draw.lines(surface, (200, 50, 50), False, points, 2)
    
    @staticmethod
    def draw_golf_ball(surface, x, y, radius):
        # White with dimples
        pygame.draw.circle(surface, (240, 240, 240), (x, y), radius)
        # Dimples
        for i in range(30):
            angle = math.radians(i * 12 + 30)
            dist = radius * 0.5 + 5 * math.sin(i * 3)
            dx = x + dist * math.cos(angle)
            dy = y + dist * math.sin(angle)
            pygame.draw.circle(surface, (200, 200, 200), (int(dx), int(dy)), 3)
    
    @staticmethod
    def draw_soccer_ball(surface, x, y, radius):
        # Classic black and white pattern
        pygame.draw.circle(surface, (255, 255, 255), (x, y), radius)
        # Black pentagon patches
        for i in range(6):
            angle = math.radians(i * 60 + 30)
            px = x + radius * 0.6 * math.cos(angle)
            py = y + radius * 0.6 * math.sin(angle)
            points = []
            for j in range(5):
                a = math.radians(j * 72 + i * 60)
                r = radius * 0.2
                points.append((px + r * math.cos(a), py + r * math.sin(a)))
            if len(points) > 2:
                pygame.draw.polygon(surface, (40, 40, 40), points)
    
    @staticmethod
    def draw_basketball(surface, x, y, radius):
        # Orange with black lines
        pygame.draw.circle(surface, (255, 140, 50), (x, y), radius)
        # Main seams
        pygame.draw.line(surface, (30, 30, 30), (x, y - radius * 0.8), (x, y + radius * 0.8), 2)
        pygame.draw.line(surface, (30, 30, 30), (x - radius * 0.8, y), (x + radius * 0.8, y), 2)
        # Curved seams
        for angle in [45, 135, 225, 315]:
            rad = math.radians(angle)
            start = (x + radius * 0.7 * math.cos(rad - 0.5), y + radius * 0.7 * math.sin(rad - 0.5))
            end = (x + radius * 0.7 * math.cos(rad + 0.5), y + radius * 0.7 * math.sin(rad + 0.5))
            pygame.draw.arc(surface, (30, 30, 30), (x-radius, y-radius, radius*2, radius*2),
                           rad - 0.5, rad + 0.5, 2)
    
    @staticmethod
    def draw_volleyball(surface, x, y, radius):
        # White/blue with distinctive panels
        pygame.draw.circle(surface, (240, 240, 240), (x, y), radius)
        # Panel lines
        for i in range(3):
            angle = math.radians(i * 60)
            pygame.draw.line(surface, (100, 150, 200), 
                           (x, y), 
                           (x + radius * 1.2 * math.cos(angle), y + radius * 1.2 * math.sin(angle)), 2)
        # Cross lines
        pygame.draw.line(surface, (100, 150, 200), 
                        (x - radius * 0.6, y - radius * 0.6), 
                        (x + radius * 0.6, y + radius * 0.6), 2)
        pygame.draw.line(surface, (100, 150, 200), 
                        (x + radius * 0.6, y - radius * 0.6), 
                        (x - radius * 0.6, y + radius * 0.6), 2)
    
    @staticmethod
    def draw_football(surface, x, y, radius):
        # Prolate spheroid (American football)
        points = []
        for i in range(0, 360, 10):
            angle = math.radians(i)
            # Stretch horizontally
            px = x + radius * 1.3 * math.cos(angle)
            py = y + radius * 0.8 * math.sin(angle)
            points.append((px, py))
        if len(points) > 2:
            pygame.draw.polygon(surface, (180, 120, 60), points)
            pygame.draw.polygon(surface, (150, 100, 40), points, 2)
        # Seam
        pygame.draw.line(surface, (200, 160, 100), (x - radius * 0.8, y), (x + radius * 0.8, y), 1)
    
    @staticmethod
    def draw_bowling_ball(surface, x, y, radius):
        # Dark with finger holes
        pygame.draw.circle(surface, (80, 40, 120), (x, y), radius)
        # Finger holes
        for dx, dy in [(-8, -6), (8, -6), (0, 2)]:
            pygame.draw.circle(surface, (40, 20, 60), (x + dx, y + dy), 4)
        # Shine
        pygame.draw.circle(surface, (150, 100, 180), 
                          (int(x - radius*0.3), int(y - radius*0.3)), 
                          int(radius*0.2))
    
    @staticmethod
    def draw_rugby_ball(surface, x, y, radius):
        # Oval with pointed ends
        points = []
        for i in range(0, 360, 10):
            angle = math.radians(i)
            px = x + radius * 1.4 * math.cos(angle)
            py = y + radius * 0.7 * math.sin(angle)
            points.append((px, py))
        if len(points) > 2:
            pygame.draw.polygon(surface, (200, 150, 100), points)
            pygame.draw.polygon(surface, (180, 130, 80), points, 2)
    
    @staticmethod
    def draw_cricket_ball(surface, x, y, radius):
        # Dark red with seam
        pygame.draw.circle(surface, (180, 50, 50), (x, y), radius)
        # Seam
        pygame.draw.line(surface, (150, 40, 40), (x - radius*0.8, y), (x + radius*0.8, y), 2)
        # Stitching
        for i in range(-3, 4):
            if i != 0:
                pygame.draw.circle(surface, (200, 80, 80), 
                                  (int(x + i*4), int(y - radius*0.6)), 1)
                pygame.draw.circle(surface, (200, 80, 80), 
                                  (int(x + i*4), int(y + radius*0.6)), 1)
    
    @staticmethod
    def draw_beach_ball(surface, x, y, radius):
        # Bright beach ball stripes
        colors = [(255, 50, 50), (255, 255, 50), (50, 50, 255), 
                  (50, 255, 50), (255, 50, 255), (50, 255, 255)]
        for i, color in enumerate(colors):
            start_angle = math.radians(i * 60)
            end_angle = math.radians((i + 1) * 60)
            points = [(x, y)]
            for a in range(int(start_angle * 10), int(end_angle * 10) + 1):
                angle = a / 10
                points.append((x + radius * math.cos(angle), y + radius * math.sin(angle)))
            if len(points) > 2:
                pygame.draw.polygon(surface, color, points)
    
    @staticmethod
    def draw_earth(surface, x, y, radius):
        # Planet Earth (the ultimate ball)
        pygame.draw.circle(surface, (50, 150, 255), (x, y), radius)
        # Continents (simplified blobs)
        continents = [
            [(0.3, 0.1), (0.5, 0.0), (0.7, 0.1), (0.6, 0.3), (0.4, 0.3)],
            [(0.1, 0.4), (0.3, 0.3), (0.4, 0.5), (0.2, 0.6)],
            [(0.6, 0.4), (0.8, 0.3), (0.9, 0.5), (0.7, 0.6)],
            [(0.2, 0.7), (0.4, 0.7), (0.5, 0.9), (0.3, 0.9)]
        ]
        for continent in continents:
            points = []
            for cx, cy in continent:
                px = x + (cx - 0.5) * radius * 2
                py = y + (cy - 0.5) * radius * 2
                points.append((px, py))
            if len(points) > 2:
                pygame.draw.polygon(surface, (50, 200, 50), points)
        # Cloud wisps
        for i in range(3):
            angle = math.radians(i * 120)
            wx = x + radius * 0.7 * math.cos(angle)
            wy = y + radius * 0.7 * math.sin(angle)
            pygame.draw.ellipse(surface, (255, 255, 255, 50), 
                              (wx - 20, wy - 5, 40, 10))

# ============ BALL CLASS ============
class Ball:
    # Map values to sports ball types
    SPORTS_MAP = {
        1: ('🎾', 'Tennis Ball', SportsBallRenderer.draw_tennis_ball),
        2: ('⚾', 'Baseball', SportsBallRenderer.draw_baseball),
        4: ('🏌️', 'Golf Ball', SportsBallRenderer.draw_golf_ball),
        8: ('⚽', 'Soccer Ball', SportsBallRenderer.draw_soccer_ball),
        16: ('🏀', 'Basketball', SportsBallRenderer.draw_basketball),
        32: ('🏐', 'Volleyball', SportsBallRenderer.draw_volleyball),
        64: ('🏈', 'Football', SportsBallRenderer.draw_football),
        128: ('🎳', 'Bowling Ball', SportsBallRenderer.draw_bowling_ball),
        256: ('🏉', 'Rugby Ball', SportsBallRenderer.draw_rugby_ball),
        512: ('🏏', 'Cricket Ball', SportsBallRenderer.draw_cricket_ball),
        1024: ('🏖️', 'Beach Ball', SportsBallRenderer.draw_beach_ball),
        2048: ('🌍', 'Earth', SportsBallRenderer.draw_earth),
    }
    
    def __init__(self, x, y, value=1):
        self.x = x
        self.y = y
        self.value = value
        self.radius = BALL_RADIUS + (value.bit_length() - 1) * 2
        self.velocity_x = 0
        self.velocity_y = 0
        self.falling = False
        self.sport_icon, self.sport_name, self.draw_func = self.SPORTS_MAP.get(
            value, ('⚪', 'Unknown', SportsBallRenderer.draw_tennis_ball)
        )
        # Glow color based on sport
        self.glow_color = self._get_glow_color()
        
    def _get_glow_color(self):
        colors = {
            1: (200, 230, 50),    # Tennis - yellow
            2: (255, 200, 200),   # Baseball - white
            4: (200, 200, 200),   # Golf - silver
            8: (50, 50, 50),      # Soccer - black/white
            16: (255, 140, 50),   # Basketball - orange
            32: (100, 150, 200),  # Volleyball - blue
            64: (180, 120, 60),   # Football - brown
            128: (80, 40, 120),   # Bowling - purple
            256: (200, 150, 100), # Rugby - tan
            512: (180, 50, 50),   # Cricket - red
            1024: (255, 100, 200),# Beach - pink
            2048: (50, 150, 255), # Earth - blue
        }
        return colors.get(self.value, (200, 200, 200))
    
    def draw(self, screen):
        # Glow effect
        glow_radius = self.radius + 10
        glow_surface = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
        glow_color = (*self.glow_color, 40)
        pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
        screen.blit(glow_surface, (self.x - glow_radius, self.y - glow_radius))
        
        # Draw the sport ball
        self.draw_func(screen, self.x, self.y, self.radius)
        
        # Add a subtle highlight
        highlight = pygame.Surface((self.radius, self.radius), pygame.SRCALPHA)
        pygame.draw.circle(highlight, (255, 255, 255, 30), 
                          (int(self.radius*0.3), int(self.radius*0.3)), 
                          int(self.radius*0.4))
        screen.blit(highlight, (self.x - int(self.radius*0.7), self.y - int(self.radius*0.7)))
        
        # Value text (with sport icon)
        font = pygame.font.Font(None, max(14, self.radius//2))
        text = font.render(f"{self.sport_icon}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(text, text_rect)
        
        # Small value number
        small_font = pygame.font.Font(None, 10)
        val_text = small_font.render(str(self.value), True, (255, 255, 255))
        val_rect = val_text.get_rect(center=(int(self.x), int(self.y + self.radius + 10)))
        screen.blit(val_text, val_rect)
    
    def merge(self, other):
        if self.value == other.value and self != other:
            dist = math.hypot(self.x - other.x, self.y - other.y)
            if dist < (self.radius + other.radius) * MERGE_THRESHOLD:
                # Merge creates next level sport ball
                return Ball((self.x + other.x)/2, (self.y + other.y)/2, self.value * 2)
        return None

# ============ GAME CLASS ============
class Game:
    def __init__(self, mode='endless'):
        self.mode = mode
        self.balls = []
        self.score = 0
        self.high_score = 0
        self.game_over = False
        self.start_time = None
        self.time_left = TIMED_MODE_DURATION
        self.dropping_ball = None
        self.drop_cooldown = 0
        self.squat_confirmed = False
        self.squat_frames = 0
        self.current_hip_pos = 0.5
        self.target_hip_pos = 0.5
        self.last_drop_pos = None
        self.merge_animation = []
        self.total_merges = 0
        
        self._spawn_initial_balls()
        
    def _spawn_initial_balls(self):
        for i in range(3):
            x = SCREEN_WIDTH//2 + (i-1) * 100
            y = GAME_AREA_TOP + 30
            self.balls.append(Ball(x, y, 1))
    
    def spawn_new_ball(self):
        x = random.randint(100, SCREEN_WIDTH - 100)
        y = GAME_AREA_TOP + 20
        # Weighted random: mostly lower values
        value = random.choices([1, 1, 1, 2, 2, 4, 8], weights=[40, 30, 20, 5, 3, 1.5, 0.5])[0]
        new_ball = Ball(x, y, value)
        self.balls.append(new_ball)
        
        # Announce new ball
        print(f"🏐 New {new_ball.sport_name} spawned! (Value: {new_ball.value})")
    
    def update(self, knee_angles, hip_center_x):
        if self.game_over:
            return
        
        # Timer for timed mode
        if self.mode == 'timed' and self.start_time:
            elapsed = time.time() - self.start_time
            self.time_left = max(0, TIMED_MODE_DURATION - elapsed)
            if self.time_left <= 0:
                self.game_over = True
                if self.score > self.high_score:
                    self.high_score = self.score
                return
        
        # Update hip position for ball movement
        if hip_center_x is not None:
            self.target_hip_pos = np.clip((hip_center_x - 0.1) / 0.8, 0, 1)
            self.current_hip_pos += (self.target_hip_pos - self.current_hip_pos) * 0.1
        
        # Move top ball horizontally
        top_balls = [b for b in self.balls if b.y < GAME_AREA_TOP + 50 and not b.falling]
        if top_balls:
            # Move the closest ball to hip position
            ball = min(top_balls, key=lambda b: abs(b.x - (50 + self.current_hip_pos * (SCREEN_WIDTH - 100))))
            ball.x = 50 + self.current_hip_pos * (SCREEN_WIDTH - 100)
        
        # Check squat for dropping (BOTH legs must be at 80°)
        if knee_angles and len(knee_angles) >= 2:
            left_knee = knee_angles[0]
            right_knee = knee_angles[1]
            
            if left_knee >= KNEE_FLEX_THRESHOLD and right_knee >= KNEE_FLEX_THRESHOLD:
                self.squat_frames += 1
                if self.squat_frames >= SQUAT_HOLD_FRAMES and not self.squat_confirmed:
                    self.squat_confirmed = True
                    self._drop_ball()
            else:
                self.squat_frames = max(0, self.squat_frames - 2)
                if self.squat_frames < SQUAT_HOLD_FRAMES // 2:
                    self.squat_confirmed = False
        
        # Update falling balls
        for ball in self.balls[:]:
            if ball.falling:
                ball.y += FALL_SPEED
                
                # Wall bouncing
                if ball.x - ball.radius < 0:
                    ball.x = ball.radius
                    ball.velocity_x *= -0.5
                elif ball.x + ball.radius > SCREEN_WIDTH:
                    ball.x = SCREEN_WIDTH - ball.radius
                    ball.velocity_x *= -0.5
                
                # Check merges
                for other in self.balls[:]:
                    if other != ball and not other.falling:
                        merged = ball.merge(other)
                        if merged:
                            # Animation effect
                            self.total_merges += 1
                            print(f"✨ MERGE! {ball.sport_name} + {other.sport_name} = {merged.sport_name} (Value: {merged.value})")
                            
                            self.balls.remove(ball)
                            self.balls.remove(other)
                            self.balls.append(merged)
                            self.score += merged.value
                            if self.score > self.high_score:
                                self.high_score = self.score
                            break
                
                # Remove if off screen
                if ball.y - ball.radius > GAME_AREA_BOTTOM:
                    if ball in self.balls:
                        self.balls.remove(ball)
                        if self.mode == 'endless':
                            self.game_over = True
                            print(f"💀 Game Over! Lost a ball!")
        
        # Spawn new balls
        active_balls = len([b for b in self.balls if not b.falling])
        if active_balls < 3 and not self.game_over:
            self.spawn_new_ball()
        
        # Drop cooldown
        if self.drop_cooldown > 0:
            self.drop_cooldown -= 1
    
    def _drop_ball(self):
        """Drop the currently held ball"""
        top_balls = [b for b in self.balls if b.y < GAME_AREA_TOP + 50 and not b.falling]
        if top_balls and self.drop_cooldown == 0:
            ball = min(top_balls, key=lambda b: abs(b.x - (50 + self.current_hip_pos * (SCREEN_WIDTH - 100))))
            ball.falling = True
            ball.velocity_x = random.uniform(-1, 1)
            self.drop_cooldown = 20
            self.last_drop_pos = ball.x
            
            print(f"🏋️ Dropped {ball.sport_name}!")
            
            # Spawn replacement
            if not self.game_over:
                self.spawn_new_ball()
    
    def draw(self, screen):
        # Draw game area with sports theme
        pygame.draw.rect(screen, (30, 35, 50), (0, GAME_AREA_TOP, SCREEN_WIDTH, GAME_AREA_BOTTOM - GAME_AREA_TOP))
        pygame.draw.rect(screen, (60, 70, 90), (0, GAME_AREA_TOP, SCREEN_WIDTH, GAME_AREA_BOTTOM - GAME_AREA_TOP), 3)
        
        # "Field" lines at bottom
        for i in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(screen, (50, 55, 70), (i, GAME_AREA_BOTTOM), (i + 20, GAME_AREA_BOTTOM), 1)
        
        # Draw all balls
        for ball in self.balls:
            ball.draw(screen)
        
        # Draw HUD
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Score
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        
        # Sport collection status
        unique_sports = len(set(b.value for b in self.balls))
        sport_text = small_font.render(f"Sports: {unique_sports}/{len(Ball.SPORTS_MAP)}", True, (200, 200, 255))
        screen.blit(sport_text, (20, 60))
        
        # Mode
        mode_text = font.render(f"Mode: {self.mode.upper()}", True, (200, 200, 255))
        screen.blit(mode_text, (20, 90))
        
        # Timer
        if self.mode == 'timed':
            timer_text = font.render(f"⏱️ {int(self.time_left)}s", True, (255, 200, 100))
            screen.blit(timer_text, (SCREEN_WIDTH - 120, 20))
        
        # High score
        high_text = font.render(f"🏆 High: {self.high_score}", True, (255, 215, 0))
        screen.blit(high_text, (SCREEN_WIDTH - 200, 60))
        
        # Squat indicator
        if self.squat_confirmed:
            squat_indicator = font.render("✅ SQUAT DROP READY!", True, (100, 255, 100))
            screen.blit(squat_indicator, (SCREEN_WIDTH//2 - 120, 10))
        elif self.squat_frames > 0:
            progress = min(1.0, self.squat_frames / SQUAT_HOLD_FRAMES)
            bar_width = 150
            bar_height = 15
            x_pos = SCREEN_WIDTH//2 - bar_width//2
            y_pos = 10
            pygame.draw.rect(screen, (50, 50, 50), (x_pos, y_pos, bar_width, bar_height))
            pygame.draw.rect(screen, (100, 255, 100), (x_pos, y_pos, bar_width * progress, bar_height))
            # Text
            squat_text = small_font.render(f"Squat {int(progress * 100)}%", True, (200, 200, 200))
            screen.blit(squat_text, (x_pos + bar_width//2 - 30, y_pos + bar_height + 5))
        
        # Instructions
        inst_font = pygame.font.Font(None, 20)
        instructions = [
            "🏋️ Side Lunge → Move ball",
            "🦵 Squat (BOTH legs 80°) → Drop",
            f"🔄 {len([b for b in self.balls if not b.falling])} balls active"
        ]
        for i, text in enumerate(instructions):
            inst = inst_font.render(text, True, (200, 200, 200))
            screen.blit(inst, (20, SCREEN_HEIGHT - 70 + i * 22))
        
        # Current sport being held
        top_balls = [b for b in self.balls if b.y < GAME_AREA_TOP + 50 and not b.falling]
        if top_balls:
            ball = min(top_balls, key=lambda b: abs(b.x - (50 + self.current_hip_pos * (SCREEN_WIDTH - 100))))
            holding_text = small_font.render(f"Holding: {ball.sport_icon} {ball.sport_name}", True, (255, 255, 200))
            screen.blit(holding_text, (SCREEN_WIDTH - 200, 90))
        
        # Game over
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))
            
            game_over_font = pygame.font.Font(None, 72)
            go_text = game_over_font.render("🏁 GAME OVER", True, (255, 200, 50))
            screen.blit(go_text, (SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT//2 - 120))
            
            score_final = font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            screen.blit(score_final, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2 - 40))
            
            sport_count = len(set(b.value for b in self.balls))
            sport_text = small_font.render(f"Sports Unlocked: {sport_count}", True, (200, 200, 255))
            screen.blit(sport_text, (SCREEN_WIDTH//2 - 70, SCREEN_HEIGHT//2))
            
            restart_font = pygame.font.Font(None, 36)
            restart_text = restart_font.render("Press R to restart | 1=Endless | 2=Timed", True, (200, 200, 255))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 + 50))

# ============ POSE PROCESSING ============
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
    
    return angle

def get_knee_angles(landmarks):
    if not landmarks:
        return None
    
    try:
        left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                   landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
        left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        
        right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                     landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        
        left_angle = calculate_angle(left_hip, left_knee, left_ankle)
        right_angle = calculate_angle(right_hip, right_knee, right_ankle)
        
        return [left_angle, right_angle]
    except:
        return None

def get_hip_center(landmarks):
    if not landmarks:
        return None
    
    try:
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
        
        center_x = (left_hip.x + right_hip.x) / 2
        return center_x
    except:
        return None

# ============ MAIN GAME LOOP ============
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("🏀 Sports Ball Merge Fitness Game")
    clock = pygame.time.Clock()
    
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    game = Game(mode='endless')
    running = True
    
    fps_counter = deque(maxlen=30)
    
    print("🏀 SPORTS BALL MERGE FITNESS GAME")
    print("=" * 50)
    print("Collect them all! Each value = different sport:")
    print("  1:🎾 2:⚾ 4:🏌️ 8:⚽ 16:🏀 32:🏐")
    print("  64:🏈 128:🎳 256:🏉 512:🏏 1024:🏖️ 2048:🌍")
    print("\nControls:")
    print("  [1] ENDLESS mode")
    print("  [2] TIMED mode (60s)")
    print("  [R] Restart")
    print("  [ESC] Quit")
    print("=" * 50)
    
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    game = Game(mode=game.mode)
                    print("🔄 Game restarted!")
                elif event.key == pygame.K_1:
                    game = Game(mode='endless')
                    print("🔁 Switched to ENDLESS mode")
                elif event.key == pygame.K_2:
                    game = Game(mode='timed')
                    game.start_time = time.time()
                    print("⏱️ Switched to TIMED mode (60 seconds)")
        
        ret, frame = cap.read()
        if not ret:
            continue
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = pose.process(rgb_frame)
        
        knee_angles = None
        hip_center = None
        
        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            knee_angles = get_knee_angles(landmarks)
            hip_center = get_hip_center(landmarks)
            
            mp_drawing.draw_landmarks(
                frame, 
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2)
            )
            
            if knee_angles:
                h, w, _ = frame.shape
                cv2.putText(frame, f"L: {knee_angles[0]:.1f}°", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                cv2.putText(frame, f"R: {knee_angles[1]:.1f}°", (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        
        game.update(knee_angles, hip_center)
        
        screen.fill((15, 20, 35))
        game.draw(screen)
        
        frame_small = cv2.resize(frame, (320, 240))
        frame_small = cv2.cvtColor(frame_small, cv2.COLOR_BGR2RGB)
        frame_surface = pygame.surfarray.make_surface(frame_small.swapaxes(0, 1))
        screen.blit(frame_surface, (SCREEN_WIDTH - 340, 20))
        
        pygame.display.flip()
        
        fps_counter.append(clock.get_fps())
        if len(fps_counter) == 30:
            avg_fps = sum(fps_counter) / 30
            pygame.display.set_caption(f"🏀 Sports Ball Merge - {avg_fps:.1f} FPS")
    
    cap.release()
    pose.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
