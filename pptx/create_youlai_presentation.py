#!/usr/bin/env python3
"""
YouLai Boot 项目框架技术介绍 PPT 生成脚本
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import argparse

def create_youlai_boot_presentation():
    # 创建新的PowerPoint演示文稿
    prs = Presentation()

    # 设置幻灯片尺寸 (宽屏 16:9)
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)

    # 幻灯片1: 封面页
    slide_layout = prs.slide_layouts[6]  # 空白布局
    slide = prs.slides.add_slide(slide_layout)

    # 背景设置
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(44, 95, 45)  # 森林绿: #2C5F2D

    # 主标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(12.33), Inches(1.5))
    title_frame = title_box.text_frame
    title_frame.clear()
    p = title_frame.paragraphs[0]
    p.text = "YouLai Boot 项目框架技术介绍"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)  # 白色

    # 副标题
    subtitle_box = slide.shapes.add_textbox(Inches(1), Inches(3), Inches(11.33), Inches(1))
    subtitle_frame = subtitle_box.text_frame
    subtitle_frame.clear()
    p = subtitle_frame.paragraphs[0]
    p.text = "基于 Spring Boot 4 & Java 17 的企业级权限管理系统"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(18)
    p.font.italic = True
    p.font.color.rgb = RGBColor(245, 245, 245)  # 浅灰色

    # 技术架构概览标题
    overview_box = slide.shapes.add_textbox(Inches(1), Inches(4.5), Inches(11.33), Inches(0.8))
    overview_frame = overview_box.text_frame
    overview_frame.clear()
    p = overview_frame.paragraphs[0]
    p.text = "技术架构概览"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)  # 白色

    # 底部信息
    footer_box = slide.shapes.add_textbox(Inches(7), Inches(7), Inches(5), Inches(0.5))
    footer_frame = footer_box.text_frame
    footer_frame.clear()
    p = footer_frame.paragraphs[0]
    p.text = "2026年3月"
    p.alignment = PP_ALIGN.RIGHT
    p.font.size = Pt(14)
    p.font.color.rgb = RGBColor(102, 102, 102)  # 深灰色

    # 幻灯片2: 项目概述
    slide = prs.slides.add_slide(slide_layout)

    # 背景设置
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)  # 浅灰色背景

    # 标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.33), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.clear()
    p = title_frame.paragraphs[0]
    p.text = "项目概述"
    p.alignment = PP_ALIGN.LEFT
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
    # 设置标题背景色
    title_shape = slide.shapes[-1]
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = RGBColor(44, 95, 45)  # 森林绿

    # 内容
    content_items = [
        ("项目定位", "基于 JDK 17、Spring Boot 4、Spring Security 构建的前后端分离单体权限管理系统"),
        ("适用场景", "适用于企业级权限管理需求，易于扩展为微服务架构"),
        ("核心特点", "安全认证、权限控制、功能完整、现代化技术栈")
    ]

    y_pos = 1.5
    for title, desc in content_items:
        # 标题框
        item_title_box = slide.shapes.add_textbox(Inches(0.8), y_pos, Inches(2.5), Inches(0.4))
        item_title_frame = item_title_box.text_frame
        item_title_frame.clear()
        p = item_title_frame.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
        # 设置背景色
        item_title_shape = slide.shapes[-1]
        item_title_shape.fill.solid()
        item_title_shape.fill.fore_color.rgb = RGBColor(151, 188, 98)  # 苔藓绿

        # 描述框
        item_desc_box = slide.shapes.add_textbox(Inches(3.5), y_pos, Inches(6), Inches(0.4))
        item_desc_frame = item_desc_box.text_frame
        item_desc_frame.word_wrap = True
        item_desc_frame.clear()
        p = item_desc_frame.paragraphs[0]
        p.text = desc
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(51, 51, 51)  # 深灰色

        y_pos += 0.8

    # 幻灯片3: 核心技术栈
    slide = prs.slides.add_slide(slide_layout)

    # 背景设置
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)  # 浅灰色背景

    # 标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.33), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.clear()
    p = title_frame.paragraphs[0]
    p.text = "核心技术栈"
    p.alignment = PP_ALIGN.LEFT
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
    # 设置标题背景色
    title_shape = slide.shapes[-1]
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = RGBColor(44, 95, 45)  # 森林绿

    # 技术栈列表
    tech_stack = [
        ("基础框架", "Spring Boot 4.0.1", RGBColor(249, 97, 103)),  # 珊瑚红
        ("编程语言", "Java 17", RGBColor(47, 60, 126)),  # 深蓝色
        ("安全框架", "Spring Security + JWT", RGBColor(249, 231, 149)),  # 金黄色
        ("持久层", "Mybatis-Plus", RGBColor(151, 188, 98)),  # 苔藓绿
        ("数据库", "MySQL", RGBColor(2, 128, 144)),  # 青绿色
        ("缓存", "Redis + Redisson", RGBColor(109, 46, 70)),  # 浆果色
        ("API文档", "Knife4j + OpenAPI", RGBColor(132, 181, 159)),  # 鼠尾草绿
        ("构建工具", "Maven", RGBColor(184, 80, 66))  # 赤土色
    ]

    y_pos = 1.5
    for i, (category, tech, color) in enumerate(tech_stack):
        row = i // 2
        col = i % 2

        x_pos = Inches(0.8) if col == 0 else Inches(5.2)

        # 类别框
        cat_box = slide.shapes.add_textbox(x_pos, Inches(y_pos + row * 0.8), Inches(3.5), Inches(0.4))
        cat_frame = cat_box.text_frame
        cat_frame.clear()
        p = cat_frame.paragraphs[0]
        p.text = category
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
        cat_shape = slide.shapes[-1]
        cat_shape.fill.solid()
        cat_shape.fill.fore_color.rgb = color

        # 技术框
        tech_box = slide.shapes.add_textbox(x_pos, Inches(y_pos + row * 0.8 + 0.4), Inches(3.5), Inches(0.4))
        tech_frame = tech_box.text_frame
        tech_frame.clear()
        p = tech_frame.paragraphs[0]
        p.text = tech
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(51, 51, 51)  # 深灰色
        tech_shape = slide.shapes[-1]
        tech_shape.fill.solid()
        tech_shape.fill.fore_color.rgb = RGBColor(242, 242, 242)  # 浅灰色

    # 幻灯片4: 安全架构
    slide = prs.slides.add_slide(slide_layout)

    # 背景设置
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)  # 浅灰色背景

    # 标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.33), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.clear()
    p = title_frame.paragraphs[0]
    p.text = "安全架构"
    p.alignment = PP_ALIGN.LEFT
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
    # 设置标题背景色
    title_shape = slide.shapes[-1]
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = RGBColor(44, 95, 45)  # 森林绿

    # 安全特性
    security_features = [
        ("认证机制", "JWT 令牌 + Redis 会话管理，支持自动续期"),
        ("权限控制", "基于 RBAC 模型，实现细粒度权限控制（接口和按钮级别）"),
        ("安全特性", "防重复提交、令牌黑名单、多端互斥管理"),
        ("安全版本", "用于按用户维度失效历史 Token（如修改密码、被管理员强制下线后）")
    ]

    y_pos = 1.5
    for title, desc in security_features:
        # 标题框
        item_title_box = slide.shapes.add_textbox(Inches(0.8), y_pos, Inches(3), Inches(0.4))
        item_title_frame = item_title_box.text_frame
        item_title_frame.clear()
        p = item_title_frame.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
        # 设置背景色
        item_title_shape = slide.shapes[-1]
        item_title_shape.fill.solid()
        item_title_shape.fill.fore_color.rgb = RGBColor(249, 97, 103)  # 珊瑚红

        # 描述框
        item_desc_box = slide.shapes.add_textbox(Inches(4), y_pos, Inches(5.5), Inches(0.4))
        item_desc_frame = item_desc_box.text_frame
        item_desc_frame.word_wrap = True
        item_desc_frame.clear()
        p = item_desc_frame.paragraphs[0]
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(51, 51, 51)  # 深灰色

        y_pos += 0.6

    # JWT认证流程
    flow_title_box = slide.shapes.add_textbox(Inches(0.8), Inches(4.5), Inches(4), Inches(0.4))
    flow_title_frame = flow_title_box.text_frame
    flow_title_frame.clear()
    p = flow_title_frame.paragraphs[0]
    p.text = "JWT认证流程:"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = RGBColor(44, 95, 45)  # 森林绿

    flow_steps = [
        "1. 登录获取JWT令牌",
        "2. 请求携带令牌",
        "3. 验证令牌有效性",
        "4. 验证权限",
        "5. 返回结果"
    ]

    y_pos = 5.0
    for step in flow_steps:
        step_box = slide.shapes.add_textbox(Inches(0.8), y_pos, Inches(4), Inches(0.3))
        step_frame = step_box.text_frame
        step_frame.clear()
        p = step_frame.paragraphs[0]
        p.text = step
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(51, 51, 51)  # 深灰色
        y_pos += 0.3

    # 幻灯片5: 功能模块
    slide = prs.slides.add_slide(slide_layout)

    # 背景设置
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)  # 浅灰色背景

    # 标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.33), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.clear()
    p = title_frame.paragraphs[0]
    p.text = "功能模块"
    p.alignment = PP_ALIGN.LEFT
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
    # 设置标题背景色
    title_shape = slide.shapes[-1]
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = RGBColor(44, 95, 45)  # 森林绿

    # 功能模块列表
    modules = [
        ("用户管理", "用户列表、新增、编辑、删除、导入导出、个人信息维护"),
        ("角色管理", "角色创建、编辑、删除、权限分配、状态管理"),
        ("菜单管理", "菜单树形结构、类型分类、按钮级权限控制"),
        ("部门管理", "部门层级结构、人员管理"),
        ("字典管理", "字典类型与字典项管理、前端组件数据源"),
        ("系统配置", "系统参数配置、配置热更新"),
        ("代码生成", "基于模板的代码生成器、快速开发"),
        ("通知公告", "系统通知发布、撤回、分级管理")
    ]

    y_pos = 1.5
    for i, (name, desc) in enumerate(modules):
        row = i // 2
        col = i % 2

        x_pos = Inches(0.8) if col == 0 else Inches(5.2)

        # 名称框
        name_box = slide.shapes.add_textbox(x_pos, Inches(y_pos + row * 1.2), Inches(3.5), Inches(0.5))
        name_frame = name_box.text_frame
        name_frame.clear()
        p = name_frame.paragraphs[0]
        p.text = name
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
        name_shape = slide.shapes[-1]
        name_shape.fill.solid()
        name_shape.fill.fore_color.rgb = RGBColor(151, 188, 98)  # 苔藓绿

        # 描述框
        desc_box = slide.shapes.add_textbox(x_pos, Inches(y_pos + row * 1.2 + 0.5), Inches(3.5), Inches(0.7))
        desc_frame = desc_box.text_frame
        desc_frame.word_wrap = True
        desc_frame.vertical_anchor = MSO_ANCHOR.TOP
        desc_frame.clear()
        p = desc_frame.paragraphs[0]
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(51, 51, 51)  # 深灰色
        desc_shape = slide.shapes[-1]
        desc_shape.fill.solid()
        desc_shape.fill.fore_color.rgb = RGBColor(242, 242, 242)  # 浅灰色

    # 幻灯片6: 技术特色与优势
    slide = prs.slides.add_slide(slide_layout)

    # 背景设置
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)  # 浅灰色背景

    # 标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.33), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.clear()
    p = title_frame.paragraphs[0]
    p.text = "技术特色与优势"
    p.alignment = PP_ALIGN.LEFT
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
    # 设置标题背景色
    title_shape = slide.shapes[-1]
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = RGBColor(44, 95, 45)  # 森林绿

    # 优势列表
    advantages = [
        ("现代化架构", "采用最新的 Spring Boot 4、Java 17 等前沿技术栈"),
        ("安全性高", "JWT + Redis 双重认证，细粒度权限控制，安全可靠"),
        ("易于扩展", "模块化设计，提供代码生成器，便于二次开发"),
        ("微服务友好", "代码结构清晰，易于拆分为微服务架构"),
        ("前后端分离", "支持主流前端框架（Vue 3、Element-Plus）"),
        ("功能完备", "权限管理、日志记录、配置管理等功能齐全")
    ]

    y_pos = 1.5
    for title, desc in advantages:
        # 背景矩形
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.8), Inches(y_pos), Inches(8.7), Inches(0.8)
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = RGBColor(242, 242, 242)  # 浅灰色
        bg_shape.line.color.rgb = RGBColor(151, 188, 98)  # 苔藓绿
        bg_shape.line.width = Pt(2)

        # 标题框
        title_box = slide.shapes.add_textbox(Inches(1), y_pos, Inches(2), Inches(0.8))
        title_frame = title_box.text_frame
        title_frame.clear()
        p = title_frame.paragraphs[0]
        p.text = title
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
        title_shape = slide.shapes[-1]
        title_shape.fill.solid()
        title_shape.fill.fore_color.rgb = RGBColor(151, 188, 98)  # 苔藓绿

        # 描述框
        desc_box = slide.shapes.add_textbox(Inches(3.2), y_pos, Inches(6.3), Inches(0.8))
        desc_frame = desc_box.text_frame
        desc_frame.word_wrap = True
        desc_frame.clear()
        p = desc_frame.paragraphs[0]
        p.text = desc
        p.font.size = Pt(12)
        p.font.color.rgb = RGBColor(51, 51, 51)  # 深灰色
        desc_frame.margin_left = 0
        desc_frame.margin_right = 0
        desc_frame.margin_top = 0
        desc_frame.margin_bottom = 0

        y_pos += 1

    # 幻灯片7: 开发特性
    slide = prs.slides.add_slide(slide_layout)

    # 背景设置
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)  # 浅灰色背景

    # 标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.33), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.clear()
    p = title_frame.paragraphs[0]
    p.text = "开发特性"
    p.alignment = PP_ALIGN.LEFT
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
    # 设置标题背景色
    title_shape = slide.shapes[-1]
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = RGBColor(44, 95, 45)  # 森林绿

    # 开发特性列表
    dev_features = [
        ("接口文档", "集成 Knife4j 实现接口文档自动生成"),
        ("代码生成", "提供基于模板的代码生成器，快速开发"),
        ("统一异常处理", "完善的全局异常处理机制"),
        ("统一响应封装", "标准化 API 响应格式"),
        ("多环境配置", "支持 dev、prod 等多种环境配置"),
        ("日志记录", "通过 @Log 注解实现操作日志记录"),
        ("AIGC集成", "支持通义千问、DeepSeek 等AI模型"),
        ("存储服务", "集成MinIO、阿里云OSS等对象存储")
    ]

    y_pos = 1.5
    for i, (feature, detail) in enumerate(dev_features):
        row = i // 2
        col = i % 2

        x_pos = Inches(0.8) if col == 0 else Inches(5.2)

        # 特性框
        feat_box = slide.shapes.add_textbox(x_pos, Inches(y_pos + row * 1.0), Inches(3.5), Inches(0.4))
        feat_frame = feat_box.text_frame
        feat_frame.clear()
        p = feat_frame.paragraphs[0]
        p.text = feature
        p.alignment = PP_ALIGN.CENTER
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
        feat_shape = slide.shapes[-1]
        feat_shape.fill.solid()
        feat_shape.fill.fore_color.rgb = RGBColor(2, 128, 144)  # 青绿色

        # 详情框
        detail_box = slide.shapes.add_textbox(x_pos, Inches(y_pos + row * 1.0 + 0.4), Inches(3.5), Inches(0.6))
        detail_frame = detail_box.text_frame
        detail_frame.word_wrap = True
        detail_frame.vertical_anchor = MSO_ANCHOR.TOP
        detail_frame.clear()
        p = detail_frame.paragraphs[0]
        p.text = detail
        p.font.size = Pt(10)
        p.font.color.rgb = RGBColor(51, 51, 51)  # 深灰色
        detail_shape = slide.shapes[-1]
        detail_shape.fill.solid()
        detail_shape.fill.fore_color.rgb = RGBColor(242, 242, 242)  # 浅灰色

    # 幻灯片8: 总结
    slide = prs.slides.add_slide(slide_layout)

    # 背景设置
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor(245, 245, 245)  # 浅灰色背景

    # 标题
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(12.33), Inches(0.8))
    title_frame = title_box.text_frame
    title_frame.clear()
    p = title_frame.paragraphs[0]
    p.text = "总结"
    p.alignment = PP_ALIGN.LEFT
    p.font.size = Pt(32)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
    # 设置标题背景色
    title_shape = slide.shapes[-1]
    title_shape.fill.solid()
    title_shape.fill.fore_color.rgb = RGBColor(44, 95, 45)  # 森林绿

    # 总结文字
    summary_intro_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.5), Inches(11), Inches(0.5))
    summary_intro_frame = summary_intro_box.text_frame
    summary_intro_frame.clear()
    p = summary_intro_frame.paragraphs[0]
    p.text = "YouLai Boot 是一个功能完善、技术先进的权限管理系统，具备以下优势："
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = RGBColor(44, 95, 45)  # 森林绿

    # 总结要点
    summary_points = [
        "1. 采用现代化技术栈，基于 Spring Boot 4 和 Java 17",
        "2. 安全性高，JWT + Redis 双重认证机制",
        "3. 权限控制精细，支持接口和按钮级别的权限控制",
        "4. 功能齐全，涵盖用户、角色、菜单、部门、字典等管理模块",
        "5. 易于扩展，提供代码生成器和模块化设计",
        "6. 适合用作企业级应用的基础框架"
    ]

    y_pos = 2.2
    for point in summary_points:
        point_box = slide.shapes.add_textbox(Inches(0.8), y_pos, Inches(12), Inches(0.4))
        point_frame = point_box.text_frame
        point_frame.clear()
        p = point_frame.paragraphs[0]
        p.text = point
        p.font.size = Pt(14)
        p.font.color.rgb = RGBColor(51, 51, 51)  # 深灰色
        y_pos += 0.4

    # 最终总结
    final_summary_box = slide.shapes.add_textbox(Inches(0.8), Inches(5.0), Inches(11.73), Inches(0.8))
    final_summary_frame = final_summary_box.text_frame
    final_summary_frame.clear()
    p = final_summary_frame.paragraphs[0]
    p.text = "适合用于快速搭建企业级应用的基础框架"
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)  # 白色
    final_summary_shape = slide.shapes[-1]
    final_summary_shape.fill.solid()
    final_summary_shape.fill.fore_color.rgb = RGBColor(151, 188, 98)  # 苔藓绿

    # 保存演示文稿
    output_file = "YouLai_Boot_技术架构介绍.pptx"
    prs.save(output_file)
    print(f"YouLai_Boot_技术架构介绍.pptx 文件已生成！")

if __name__ == "__main__":
    create_youlai_boot_presentation()