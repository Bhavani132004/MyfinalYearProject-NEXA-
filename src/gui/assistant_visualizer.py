
"""Interactive human-like assistant visualizer"""

from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, pyqtProperty, QPointF, QEasingCurve
from PyQt5.QtGui import QPainter, QColor, QRadialGradient, QBrush, QPen
import math
import random

class AssistantVisualizer(QWidget):
    """
    A modern, human-like assistant visualizer with smooth animations.
    States: IDLE, LISTENING, THINKING, SPEAKING
    """
    
    IDLE = 0
    LISTENING = 1
    THINKING = 2
    SPEAKING = 3

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(250, 250)
        self._state = self.IDLE
        self._phase = 0.0
        self._pulse = 1.0
        self._rotation = 0.0
        self._energy = 0.0
        self._target_energy = 0.0
        self._particles = []
        
        # Animation timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._animate)
        self.timer.start(16) # ~60 FPS
        
        # Core color palette (Catppuccin Mocha inspired)
        self.colors = {
            self.IDLE: QColor("#45475a"),        # Surface1 (Dim)
            self.LISTENING: QColor("#89b4fa"),   # Blue
            self.THINKING: QColor("#fab387"),    # Peach
            self.SPEAKING: QColor("#a6e3a1")     # Green
        }
        
        self._current_color = self.colors[self.IDLE]
        self._target_color = self.colors[self.IDLE]
        
        # Breath animation
        self.breath_anim = QPropertyAnimation(self, b"pulse")
        self.breath_anim.setDuration(3000)
        self.breath_anim.setStartValue(0.95)
        self.breath_anim.setEndValue(1.05)
        self.breath_anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.breath_anim.setLoopCount(-1)
        self.breath_anim.start()
        
        self.init_particles()

    def init_particles(self):
        self._particles = []
        for _ in range(25):
            self._particles.append({
                'angle': random.uniform(0, 2 * math.pi),
                'dist': random.uniform(60, 110),
                'speed': random.uniform(0.005, 0.02),
                'size': random.uniform(1.5, 3.5),
                'opacity': random.uniform(0.2, 0.6)
            })

    @pyqtProperty(float)
    def pulse(self):
        return self._pulse

    @pulse.setter
    def pulse(self, value):
        self._pulse = value
        self.update()

    def set_state(self, state):
        if state in self.colors:
            self._state = state
            self._target_color = self.colors[state]
            
            # Reset energy when not listening
            if state != self.LISTENING:
                self._target_energy = 0.0
            
            # Adjust breath speed based on state
            if state == self.LISTENING:
                self.breath_anim.setDuration(1200) 
            elif state == self.THINKING:
                self.breath_anim.setDuration(600)  
            elif state == self.SPEAKING:
                self.breath_anim.setDuration(1000)
            else:
                self.breath_anim.setDuration(3000) 
                
            self.update()

    def set_energy(self, level):
        """Update audio energy level (0.0 to 1.0)"""
        self._target_energy = max(0.0, min(1.0, level))

    def _animate(self):
        self._phase += 0.05
        self._rotation += 3.0
        
        # Smooth color transition
        r = self._current_color.red() + (self._target_color.red() - self._current_color.red()) * 0.15
        g = self._current_color.green() + (self._target_color.green() - self._current_color.green()) * 0.15
        b = self._current_color.blue() + (self._target_color.blue() - self._current_color.blue()) * 0.15
        self._current_color = QColor(int(r), int(g), int(b))
        
        # Smooth energy transition (reacts fast to peaks, decays slower)
        decay = 0.15 if self._target_energy > self._energy else 0.08
        self._energy += (self._target_energy - self._energy) * decay
        
        # Update particles
        for p in self._particles:
            p['angle'] += p['speed'] * (1.0 + self._energy * 2.0)
            
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        cx, cy = self.width() / 2, self.height() / 2
        # Base scale accounts for breathing + audio energy
        scale = self._pulse * (1.0 + self._energy * 0.4)
        base_radius = min(cx, cy) * 0.35 * scale
        
        # 1. Background Outer Glow
        glow = QRadialGradient(cx, cy, base_radius * 2.0)
        color_with_alpha = QColor(self._current_color)
        color_with_alpha.setAlpha(int(40 + 60 * self._energy))
        glow.setColorAt(0, color_with_alpha)
        glow.setColorAt(0.6, QColor(0,0,0,0))
        glow.setColorAt(1, Qt.transparent)
        painter.setBrush(QBrush(glow))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPointF(cx, cy), base_radius * 2.5, base_radius * 2.5)

        # 2. Particle Ring
        for p in self._particles:
            orbit = p['dist'] * scale
            px = cx + math.cos(p['angle']) * orbit
            py = cy + math.sin(p['angle']) * orbit
            p_color = QColor(self._current_color)
            p_color.setAlpha(int(p['opacity'] * 255))
            painter.setBrush(QBrush(p_color))
            painter.drawEllipse(QPointF(px, py), p['size'], p['size'])

        # 3. State-specific animations
        if self._state == self.THINKING:
            self._draw_thinking(painter, cx, cy, base_radius)
        elif self._state == self.SPEAKING:
            self._draw_speaking(painter, cx, cy, base_radius)
        elif self._state == self.LISTENING:
            self._draw_listening(painter, cx, cy, base_radius)
        else:
            self._draw_idle(painter, cx, cy, base_radius)

    def _draw_idle(self, painter, cx, cy, radius):
        # Soft core with gradient
        grad = QRadialGradient(cx, cy, radius)
        grad.setColorAt(0, self._current_color)
        grad.setColorAt(1, self._current_color.darker(140))
        painter.setBrush(QBrush(grad))
        painter.setPen(QPen(self._current_color.lighter(120), 1))
        painter.drawEllipse(QPointF(cx, cy), radius, radius)

    def _draw_listening(self, painter, cx, cy, radius):
        # Pulsing concentric rings reacting to energy
        for i in range(3):
            ring_radius = radius + (i + 1) * 15 + (self._energy * 40 * (i+1)/3)
            opacity = max(20, 180 - (i * 50))
            
            pen = QPen(self._current_color, 2 + self._energy * 3)
            c = QColor(self._current_color)
            c.setAlpha(int(opacity))
            pen.setColor(c)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawEllipse(QPointF(cx, cy), ring_radius, ring_radius)
            
        self._draw_idle(painter, cx, cy, radius)

    def _draw_thinking(self, painter, cx, cy, radius):
        # Orbiting dots that pulse
        for i in range(3):
            angle = math.radians(self._rotation + (i * 120))
            dist = radius + 30 + math.sin(self._phase * 2 + i) * 10
            px = cx + math.cos(angle) * dist
            py = cy + math.sin(angle) * dist
            
            dot_color = QColor(self._current_color)
            painter.setBrush(QBrush(dot_color))
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(QPointF(px, py), 6, 6)
            
        self._draw_idle(painter, cx, cy, radius)

    def _draw_speaking(self, painter, cx, cy, radius):
        # Dynamic wave center
        pen = QPen(self._current_color, 3, Qt.SolidLine, Qt.RoundCap)
        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        
        points = []
        width_px = radius * 1.2
        for i in range(int(-width_px), int(width_px) + 1, 4):
            x = cx + i
            # Wave amplitude syncs with pulse, creates speaking "patter"
            amplitude = 15 * math.sin(self._phase * 5) * (1.0 - abs(i/width_px))
            wave = math.sin(self._phase * 3 + i * 0.1) * amplitude
            y = cy + wave
            points.append(QPointF(x, y))
            
        for i in range(len(points) - 1):
            painter.drawLine(points[i], points[i+1])
            
        self._draw_idle(painter, cx, cy, radius * 0.8)
