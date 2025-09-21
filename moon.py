import matplotlib
matplotlib.use('Agg') # 在导入 pyplot 之前设置后端
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import math
import imageio.v2 as imageio # 导入 imageio 库，用于制作GIF或MP4
import os # 用于文件操作，如清理临时帧

# 设置中文字体支持
# 在服务器上，如果中文字体不存在，可能会有问题。
# 可以考虑在生成图片时暂时移除中文，或者确保服务器安装了对应的字体。
# 也可以将字体设置为'DejaVu Sans'或其他英文通用字体。
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Microsoft YaHei'] # 优先使用服务器可能有的字体
plt.rcParams['axes.unicode_minus'] = False

# 生成模拟的月相数据（2023年）
def generate_moon_data(year=2023):
    """
    生成一年的月相数据（模拟）
    返回日期列表和对应的月相照度（0-1之间）
    """
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    delta = timedelta(days=1)
    
    dates = []
    illuminations = []
    
    current_date = start_date
    while current_date <= end_date:
        dates.append(current_date)
        # 模拟月相变化（正弦函数，周期约29.5天）
        day_of_year = current_date.timetuple().tm_yday
        # 基本正弦波模拟月相
        illumination = 0.5 * (1 + np.sin(2 * np.pi * day_of_year / 29.53 - np.pi/2))
        illuminations.append(illumination)
        current_date += delta
        
    return dates, illuminations

# 创建自定义颜色映射
def create_moon_colormap():
    """创建蓝-白-金的月相颜色映射"""
    colors = ['#0d3b66', '#1e5b8e', '#faf0ca', '#f4d35e', '#ee964b']
    return LinearSegmentedColormap.from_list('moon_phase', colors, N=256)

# 修改后的主可视化函数，用于生成动画帧
def create_moon_phase_animation(dates, illuminations, year=2023, frame_rate=10):
    """
    创建月相极坐标动画，展示月亮围绕中心旋转。
    frame_rate: 每秒帧数，决定动画流畅度。
    """
    fig = plt.figure(figsize=(10, 10), facecolor='#0d1b2a')
    ax = plt.subplot(111, projection='polar', facecolor='#0d1b2a')
    
    cmap = create_moon_colormap()
    
    days_in_year = 365 if year % 4 != 0 else 366
    theta_full = np.linspace(0, 2*np.pi, days_in_year, endpoint=False)
    radii_full = np.ones(days_in_year)
    
    # 绘制基础的暗色圆环，代表整个年份的轨道
    ax.scatter(theta_full, radii_full, c=illuminations, 
               cmap=cmap, s=30, alpha=0.2, zorder=1) # 基础层，透明度降低，zorder较低
    
    # 设置极坐标图的样式
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_ylim(0, 1.1)
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(False)
    ax.spines['polar'].set_visible(False)
    
    # 添加月份标签
    month_angles = []
    import calendar
    month_names = [calendar.month_abbr[m] for m in range(1, 13)]
    for month in range(1, 13):
        first_day = datetime(year, month, 1)
        day_of_year = first_day.timetuple().tm_yday
        days_in_month = (datetime(year, month+1, 1) if month < 12 
                         else datetime(year+1, 1, 1)) - first_day
        angle = 2 * np.pi * (day_of_year + days_in_month.days/2) / days_in_year
        month_angles.append(angle)
    
    month_texts = []
    for angle, name in zip(month_angles, month_names):
        text = ax.text(angle, 1.08, name, ha='center', va='center',
                       color='#e0e1dd', fontsize=11, fontweight='bold', 
                       rotation=np.degrees(angle)-90, rotation_mode='anchor')
        month_texts.append(text)
    
    # 添加标题和年份
    title_text = plt.figtext(0.5, 0.90, f'{year} Lunar Phase Changes for New York, USA', 
                             ha='center', color='#e0e1dd', fontsize=16, fontweight='bold')
    
    # 添加颜色条 (只显示一次，不随帧变化)
    cbar_ax = fig.add_axes([0.15, 0.02, 0.7, 0.03])
    scatter_cbar_ref = ax.scatter(np.linspace(0, 2*np.pi, days_in_year, endpoint=False), np.ones(days_in_year), c=illuminations, 
                         cmap=cmap, s=15, alpha=0.9)
    cbar = plt.colorbar(scatter_cbar_ref, cax=cbar_ax, orientation='horizontal')
    cbar.set_label('Lunar Illumination', color='#e0e1dd', fontsize=12)
    cbar.ax.tick_params(colors='#e0e1dd')
    cbar.set_ticks([0, 0.25, 0.5, 0.75, 1])
    cbar.set_ticklabels(['New Moon', 'First Quarter', 'Full Moon', 'Last Quarter', 'New Moon'])
    
    moon_marker = cbar_ax.scatter([0.5], [0.5], color='#faf0ca', s=300, edgecolor='white', linewidths=3, zorder=5)


    # 添加一些装饰性的星星 (只绘制一次)
    star_x, star_y, star_s, star_alpha = [], [], [], []
    for _ in range(50):
        angle = np.random.uniform(0, 2*np.pi)
        r = np.random.uniform(1.05, 1.25)
        size = np.random.uniform(1, 4)
        brightness = np.random.uniform(0.6, 1.0)
        # 将极坐标转换为笛卡尔坐标以绘制星星
        x_cart = r * np.cos(angle)
        y_cart = r * np.sin(angle)
        star_x.append(x_cart)
        star_y.append(y_cart)
        star_s.append(size)
        star_alpha.append(brightness)

    star_theta = np.random.uniform(0, 2*np.pi, 50)
    star_r = np.random.uniform(1.05, 1.25, 50)
    star_s = np.random.uniform(1, 4, 50)
    star_alpha = np.random.uniform(0.6, 1.0, 50)
    ax.scatter(star_theta, star_r, s=star_s, color='white', marker='*', alpha=star_alpha, zorder=0)

    # 准备动画帧
    frames = []
    frame_dir = f'moon_animation_frames_{year}'
    os.makedirs(frame_dir, exist_ok=True)
    
    # 用来高亮显示当前月相的散点图对象
    # 注意：在极坐标图中使用 ax.plot(theta, r)
    current_moon_plot, = ax.plot([], [], 'o', color='#faf0ca', markersize=20, 
                                 zorder=3, markeredgecolor='white', markeredgewidth=2)
    
    # 用来显示当前日期的文本
    # 放置在图表中心，为了不与极坐标冲突，可以调整其位置
    current_date_text = ax.text(0, 0, '', ha='center', va='center', 
                                color='#faf0ca', fontsize=14, fontweight='bold', zorder=4)

    # 动画主循环：每天生成一帧
    for i, (date, illumination) in enumerate(zip(dates, illuminations)):
        # 更新高亮显示
        theta_current = theta_full[i]
        radius_current = radii_full[i]
        
        # 更新月亮位置和颜色
        current_moon_plot.set_data([theta_current], [radius_current])
        current_moon_plot.set_markerfacecolor(cmap(illumination))
        
        # 更新日期文本
        current_date_text.set_text(date.strftime('%Y-%m-%d'))

        moon_marker.set_offsets([[illumination, 0.5]])
        moon_marker.set_facecolor(cmap(illumination))
        
        # 保存当前帧
        frame_filename = os.path.join(frame_dir, f'frame_{i:04d}.png')
        plt.savefig(frame_filename, dpi=100, bbox_inches='tight', 
                    facecolor=fig.get_facecolor(), edgecolor='none')
        frames.append(frame_filename)
        
    plt.close(fig) # 关闭图表，释放内存

    # 将帧合成为MP4视频
    mp4_filename = f'moon_phase_animation_{year}.mp4'
    print(f"Generating MP4: {mp4_filename}...")
    try:
        # imageio.get_writer 需要安装合适的 ffmpeg 后端
        # 可以通过 `imageio.plugins.ffmpeg.download()` 下载或手动安装
        with imageio.get_writer(mp4_filename, mode='I', fps=frame_rate, codec='libx264') as writer:
            for filename in frames:
                image = imageio.imread(filename)
                if image.shape[-1] == 4:
                    image = image[..., :3]  # 丢弃alpha通道
                writer.append_data(image)
        print("MP4 generation complete.")
    except Exception as e:
        print(f"Error generating MP4: {e}")
        print("Please ensure you have ffmpeg installed and available in your PATH,")
        print("or use 'imageio.plugins.ffmpeg.download()' to install it.")

    # 可选：清理临时帧文件
    for filename in frames:
        os.remove(filename)
    os.rmdir(frame_dir)
    print(f"Cleaned up temporary frames in {frame_dir}.")


def generate_moon_data_from_csv(csv_filepath, year=2024):
    """
    从 CSV 文件中读取月相数据，自动补齐全年数据并插值缺失值
    返回日期列表和对应的月相照度（0-1之间）
    """
    df = pd.read_csv(csv_filepath)
    
    # 只保留 Line == 1 的行
    df = df[df['Line'] == 1]
    
    # 转换日期格式
    df['Date'] = pd.to_datetime(df['Date'])
    
    # 只取目标年份
    df = df[df['Date'].dt.year == year]
    
    # 转换 Illuminated（去掉 %，变成浮点数）
    df['Illuminated'] = df['Illuminated'].str.rstrip('%').astype(float)
    
    # 创建全年日期索引（闰年 366 天）
    full_dates = pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="D")
    
    # 对齐全年日期
    df = df.set_index('Date').reindex(full_dates)
    
    # 插值填充缺失值
    df['Illuminated'] = df['Illuminated'].interpolate(limit_direction='both')
    
    # 转换到 0-1 范围
    illuminations = (df['Illuminated'] / 100).tolist()
    
    return full_dates.tolist(), illuminations


if __name__ == "__main__":
    year = 2024  # 根据 CSV 文件年份调整
    csv_filepath = 'astro-202401-202412.csv'  # CSV 文件路径
    dates, illuminations = generate_moon_data_from_csv(csv_filepath)
    create_moon_phase_animation(dates, illuminations, year, frame_rate=15)  # 提高帧率使动画更流畅
