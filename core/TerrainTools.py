import numpy as np              # 地形数据存储与矩阵运算
import scipy.ndimage as ndi     # 图像处理与滤波

class TerrainTools:
    @staticmethod
    def apply_filter(heightmap, filter_type='gaussian', sigma=1.0):
        """应用各种滤波器"""
        if filter_type == 'gaussian':
            return ndi.gaussian_filter(heightmap, sigma=sigma)
        elif filter_type == 'median':
            return ndi.median_filter(heightmap, size=3)
        elif filter_type == 'ridge':
            # 山脊增强
            from scipy import signal
            kernel = np.array([[-1, -1, -1],
                               [-1,  8, -1],
                               [-1, -1, -1]])
            return signal.convolve2d(heightmap, kernel, mode='same')
    
    @staticmethod
    def calculate_shadow_map(heightmap, light_angle=45):
        """生成阴影图（类似Wilbur的渲染）"""
        light_rad = np.deg2rad(light_angle)
        dx = np.cos(light_rad)
        dy = np.sin(light_rad)
        
        gradient_x, gradient_y = np.gradient(heightmap)
        shade = dx * gradient_x + dy * gradient_y
        shade = (shade - shade.min()) / (shade.max() - shade.min())
        return 1 - shade  # 反转使阴影更直观
    
    @staticmethod
    def export_heightmap(heightmap, filename, format='npy'):
        """导出高度图"""
        if format == 'npy':
            np.save(filename, heightmap)
        elif format == 'png':
            import imageio
            normalized = (heightmap - heightmap.min()) / (heightmap.max() - heightmap.min())
            imageio.imwrite(filename, (normalized * 255).astype(np.uint8))
