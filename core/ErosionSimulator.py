import numpy as np              # 地形数据存储与矩阵运算
import scipy.ndimage as ndi     # 图像处理与滤波

class ErosionSimulator:
    def __init__(self, heightmap):
        self.heightmap = heightmap.copy()
        self.watermap = np.zeros_like(heightmap)
        self.sediment = np.zeros_like(heightmap)
        
    def hydraulic_erosion(self, iterations=1000, rain_rate=0.01, evaporation=0.9, capacity=0.1):
        """水力侵蚀模拟"""
        for _ in range(iterations):
            # 1. 添加雨水
            self.watermap += rain_rate
            
            # 2. 计算水流方向（D8算法）
            water_flow = self.calculate_water_flow()
            
            # 3. 计算流速和侵蚀能力
            erosion_rate, deposition_rate = self.calculate_erosion_rate(water_flow)
            
            # 4. 侵蚀与沉积
            self.heightmap -= erosion_rate
            self.sediment += erosion_rate - deposition_rate
            
            # 5. 蒸发
            self.watermap *= evaporation
            
        return self.heightmap
    
    def calculate_water_flow(self):
        """计算水流方向 - D8算法"""
        gradients = np.gradient(self.heightmap + self.watermap * 0.1)
        flow = np.sqrt(gradients[0]**2 + gradients[1]**2)
        return flow
    
    def thermal_erosion(self, iterations=100, talus_angle=30):
        """热力侵蚀（物质滑落）"""
        height_radians = np.deg2rad(talus_angle)
        
        for _ in range(iterations):
            # 计算坡度
            dy, dx = np.gradient(self.heightmap)
            slope = np.sqrt(dx**2 + dy**2)
            
            # 超过临界坡度的物质滑落
            mask = slope > np.tan(height_radians)
            
            # 物质从高处向低处移动
            if np.any(mask):
                blurred = ndi.gaussian_filter(self.heightmap, sigma=0.5)
                self.heightmap[mask] = blurred[mask]
                
        return self.heightmap
    
    def river_erosion(self, start_points, iterations=1000):
        """河道侵蚀模拟"""
        for start in start_points:
            x, y = start
            for _ in range(iterations):
                # 寻找最陡下降方向
                neighbors = [
                    (x-1, y-1), (x-1, y), (x-1, y+1),
                    (x, y-1),             (x, y+1),
                    (x+1, y-1), (x+1, y), (x+1, y+1)
                ]
                
                # 计算梯度并选择方向
                min_height = self.heightmap[x, y]
                next_pos = (x, y)
                
                for nx, ny in neighbors:
                    if 0 <= nx < self.heightmap.shape[0] and 0 <= ny < self.heightmap.shape[1]:
                        if self.heightmap[nx, ny] < min_height:
                            min_height = self.heightmap[nx, ny]
                            next_pos = (nx, ny)
                
                # 侵蚀当前位置
                self.heightmap[x, y] -= 0.01
                
                # 移动到下一个位置
                x, y = next_pos
                
        return self.heightmap
