import numpy as np              # 地形数据存储与矩阵运算
import noise                    # Perlin噪声生成

class TerrainGenerator:
    def __init__(self, width=1024, height=1024):
        self.heightmap = np.zeros((height, width))
        
    def perlin_noise(self, scale=100.0, octaves=6, persistence=0.5, lacunarity=2.0):
        """分形噪声生成基础地形"""
        for i in range(self.heightmap.shape[0]):
            for j in range(self.heightmap.shape[1]):
                self.heightmap[i][j] = noise.pnoise2(
                    i/scale, j/scale, 
                    octaves=octaves,
                    persistence=persistence,
                    lacunarity=lacunarity,
                    repeatx=1024,
                    repeaty=1024
                )
        return self.normalize_heightmap()
    
    def fault_formation(self, iterations=1000):
        """断层线生成地形"""
        for _ in range(iterations):
            # 随机生成一条断层线
            angle = np.random.random() * 2 * np.pi
            distance = np.random.random() * np.sqrt(self.heightmap.shape[0]**2 + self.heightmap.shape[1]**2)
            
            # 计算点到线的距离
            for i in range(self.heightmap.shape[0]):
                for j in range(self.heightmap.shape[1]):
                    d = j * np.cos(angle) + i * np.sin(angle) - distance
                    if d > 0:
                        self.heightmap[i, j] += 0.01  # 一侧抬升
        return self.heightmap
    
    def normalize_heightmap(self):
        """归一化高度图到[0,1]范围"""
        self.heightmap = (self.heightmap - self.heightmap.min()) / (self.heightmap.max() - self.heightmap.min())
        return self.heightmap
