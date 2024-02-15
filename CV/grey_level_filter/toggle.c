<<<<<<< HEAD
#include<stdio.h>
#include<libjpeg>

=======
#include <stdio.h>
#include <stdlib.h>
#include <jpeglib.h>
/********************************
 * from gpt
 * 
 * 
**********************************/
typedef struct {
    unsigned char r, g, b;
} RGBPixel;

RGBPixel* read_jpeg(const char* filename, int* width, int* height) {
    // 打开 JPEG 文件
    FILE* file = fopen(filename, "rb");
    if (!file) {
        printf("Failed to open the file.\n");
        return NULL;
    }

    // 创建 JPEG 解码器
    struct jpeg_decompress_struct cinfo;
    struct jpeg_error_mgr jerr;
    cinfo.err = jpeg_std_error(&jerr);
    jpeg_create_decompress(&cinfo);

    // 指定输入文件
    jpeg_stdio_src(&cinfo, file);

    // 读取 JPEG 文件的头信息
    jpeg_read_header(&cinfo, TRUE);
    *width = cinfo.image_width;
    *height = cinfo.image_height;

    // 开始解压缩
    jpeg_start_decompress(&cinfo);

    // 分配内存以存储像素数据
    RGBPixel* pixels = (RGBPixel*)malloc(*width * *height * sizeof(RGBPixel));
    if (!pixels) {
        printf("Memory allocation failed.\n");
        jpeg_destroy_decompress(&cinfo);
        fclose(file);
        return NULL;
    }

    // 读取像素数据
    JSAMPARRAY buffer = (JSAMPARRAY)malloc(sizeof(JSAMPROW) * cinfo.output_height);
    for (int i = 0; i < cinfo.output_height; ++i) {
        buffer[i] = (JSAMPROW)calloc(cinfo.output_width * cinfo.output_components, sizeof(JSAMPLE));
    }

    int row = 0;
    while (cinfo.output_scanline < cinfo.output_height) {
        jpeg_read_scanlines(&cinfo, buffer + row, cinfo.output_height - row);
        row += cinfo.output_height - row;
    }

    // 将像素数据转换为 RGB 格式
    for (int y = 0; y < *height; ++y) {
        for (int x = 0; x < *width; ++x) {
            pixels[y * *width + x].r = buffer[y][x * cinfo.output_components];
            pixels[y * *width + x].g = buffer[y][x * cinfo.output_components + 1];
            pixels[y * *width + x].b = buffer[y][x * cinfo.output_components + 2];
        }
    }

    // 完成解压缩
    jpeg_finish_decompress(&cinfo);

    // 释放资源
    for (int i = 0; i < cinfo.output_height; ++i) {
        free(buffer[i]);
    }
    free(buffer);

    jpeg_destroy_decompress(&cinfo);
    fclose(file);

    return pixels;
}

int main() {
    const char* filename = "example.jpg"; // 替换为您的 JPEG 图像文件路径
    int width, height;

    // 读取 JPEG 图像文件并获取宽度和高度
    RGBPixel* pixels = read_jpeg(filename, &width, &height);
    if (!pixels) {
        return -1;
    }

    // 打印图像宽度和高度
    printf("Image width: %d, height: %d\n", width, height);

    // 打印前几行像素值
    printf("Pixel values:\n");
    for (int y = 0; y < 3 && y < height; ++y) { // 打印前三行
        for (int x = 0; x < 3 && x < width; ++x) { // 打印前三列
            RGBPixel pixel = pixels[y * width + x];
            printf("(%3d, %3d, %3d) ", pixel.r, pixel.g, pixel.b);
        }
        printf("\n");
    }

    // 释放内存
    free(pixels);

    return 0;
}
>>>>>>> ee2759fe692d73f8c5275da5cb769c93ae24e899
