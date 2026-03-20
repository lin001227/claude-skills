// 使用PPTXGenJS创建YouLai Boot项目框架技术介绍演示文稿
const fs = require('fs');

// 检查是否已安装pptxgenjs
let pptx;
try {
    pptx = require('pptxgenjs');
} catch (e) {
    // 尝试从全局安装路径加载
    try {
        pptx = require('C:/Users/linxianhan/AppData/Roaming/npm/node_modules/pptxgenjs');
    } catch (e2) {
        console.error('未能加载pptxgenjs模块，请确保已安装:', e.message, e2.message);
        process.exit(1);
    }
}

// 创建一个新的PowerPoint演示文稿
const pres = new pptx();

// 幻灯片1: 封面页
let slide = pres.addSlide();
slide.addText('YouLai Boot 项目框架技术介绍', {
    x: 0.5,
    y: 1.5,
    w: 12,
    h: 1.5,
    fontSize: 36,
    bold: true,
    color: 'FFFFFF',
    fill: { color: '2C5F2D' }, // 森林绿
    align: 'center',
    valign: 'middle'
});

slide.addText('基于 Spring Boot 4 & Java 17 的企业级权限管理系统', {
    x: 1,
    y: 3,
    w: 11.33,
    h: 1,
    fontSize: 18,
    italic: true,
    color: '2C5F2D',
    align: 'center'
});

slide.addText('技术架构概览', {
    x: 1,
    y: 4.5,
    w: 11.33,
    h: 0.8,
    fontSize: 24,
    bold: true,
    color: 'F5F5F5',
    fill: { color: '97BC62' }, // 苔藓绿
    align: 'center'
});

slide.addText('2026年3月', {
    x: 10,
    y: 6.5,
    fontSize: 14,
    color: '666666',
    align: 'right'
});

// 幻灯片2: 项目概述
slide = pres.addSlide();
slide.addText('项目概述', {
    x: 0.5,
    y: 0.3,
    w: 12.33,
    h: 0.8,
    fontSize: 32,
    bold: true,
    color: 'FFFFFF',
    fill: { color: '2C5F2D' },
    align: 'left'
});

const overviewContent = [
    { title: '项目定位', desc: '基于 JDK 17、Spring Boot 4、Spring Security 构建的前后端分离单体权限管理系统' },
    { title: '适用场景', desc: '适用于企业级权限管理需求，易于扩展为微服务架构' },
    { title: '核心特点', desc: '安全认证、权限控制、功能完整、现代化技术栈' }
];

let yPosition = 1.5;
for (const item of overviewContent) {
    slide.addText(item.title, {
        x: 0.8,
        y: yPosition,
        w: 2.5,
        h: 0.4,
        fontSize: 16,
        bold: true,
        color: 'FFFFFF',
        fill: { color: '97BC62' },
        align: 'center',
        valign: 'middle'
    });

    slide.addText(item.desc, {
        x: 3.5,
        y: yPosition,
        w: 6,
        h: 0.4,
        fontSize: 14,
        color: '333333',
        valign: 'middle'
    });

    yPosition += 0.8;
}

// 幻灯片3: 核心技术栈
slide = pres.addSlide();
slide.addText('核心技术栈', {
    x: 0.5,
    y: 0.3,
    w: 12.33,
    h: 0.8,
    fontSize: 32,
    bold: true,
    color: 'FFFFFF',
    fill: { color: '2C5F2D' },
    align: 'left'
});

const techStack = [
    { category: '基础框架', tech: 'Spring Boot 4.0.1', color: 'F96167' },
    { category: '编程语言', tech: 'Java 17', color: '2F3C7E' },
    { category: '安全框架', tech: 'Spring Security + JWT', color: 'F9E795' },
    { category: '持久层', tech: 'Mybatis-Plus', color: '97BC62' },
    { category: '数据库', tech: 'MySQL', color: '028090' },
    { category: '缓存', tech: 'Redis + Redisson', color: '6D2E46' },
    { category: 'API文档', tech: 'Knife4j + OpenAPI', color: '84B59F' },
    { category: '构建工具', tech: 'Maven', color: 'B85042' }
];

yPosition = 1.5;
for (let i = 0; i < techStack.length; i++) {
    const item = techStack[i];
    const row = Math.floor(i / 2);
    const col = i % 2;

    slide.addText(item.category, {
        x: col === 0 ? 0.8 : 5.2,
        y: yPosition + row * 0.8,
        w: 3.5,
        h: 0.4,
        fontSize: 14,
        bold: true,
        color: 'FFFFFF',
        fill: { color: item.color },
        align: 'center',
        valign: 'middle'
    });

    slide.addText(item.tech, {
        x: col === 0 ? 0.8 : 5.2,
        y: yPosition + row * 0.8 + 0.4,
        w: 3.5,
        h: 0.4,
        fontSize: 14,
        color: '333333',
        fill: { color: 'F2F2F2' },
        align: 'center',
        valign: 'middle'
    });
}

// 幻灯片4: 安全架构
slide = pres.addSlide();
slide.addText('安全架构', {
    x: 0.5,
    y: 0.3,
    w: 12.33,
    h: 0.8,
    fontSize: 32,
    bold: true,
    color: 'FFFFFF',
    fill: { color: '2C5F2D' },
    align: 'left'
});

const securityFeatures = [
    { title: '认证机制', desc: 'JWT 令牌 + Redis 会话管理，支持自动续期' },
    { title: '权限控制', desc: '基于 RBAC 模型，实现细粒度权限控制（接口和按钮级别）' },
    { title: '安全特性', desc: '防重复提交、令牌黑名单、多端互斥管理' },
    { title: '安全版本', desc: '用于按用户维度失效历史 Token（如修改密码、被管理员强制下线后）' }
];

yPosition = 1.5;
for (const feature of securityFeatures) {
    slide.addText(feature.title, {
        x: 0.8,
        y: yPosition,
        w: 3,
        h: 0.4,
        fontSize: 14,
        bold: true,
        color: 'FFFFFF',
        fill: { color: 'F96167' },
        align: 'center',
        valign: 'middle'
    });

    slide.addText(feature.desc, {
        x: 4,
        y: yPosition,
        w: 5.5,
        h: 0.4,
        fontSize: 12,
        color: '333333',
        fill: { color: 'F2F2F2' },
        valign: 'middle'
    });

    yPosition += 0.6;
}

// 添加流程图
slide.addText('JWT认证流程:', {
    x: 0.8,
    y: 4.5,
    fontSize: 14,
    bold: true,
    color: '2C5F2D'
});

const flowSteps = [
    '1. 登录获取JWT令牌',
    '2. 请求携带令牌',
    '3. 验证令牌有效性',
    '4. 验证权限',
    '5. 返回结果'
];

yPosition = 5;
for (const step of flowSteps) {
    slide.addText(step, {
        x: 0.8,
        y: yPosition,
        fontSize: 12,
        color: '333333',
        bullet: { code: '2022' } // 使用圆点作为项目符号
    });
    yPosition += 0.3;
}

// 幻灯片5: 功能模块
slide = pres.addSlide();
slide.addText('功能模块', {
    x: 0.5,
    y: 0.3,
    w: 12.33,
    h: 0.8,
    fontSize: 32,
    bold: true,
    color: 'FFFFFF',
    fill: { color: '2C5F2D' },
    align: 'left'
});

const modules = [
    { name: '用户管理', desc: '用户列表、新增、编辑、删除、导入导出、个人信息维护' },
    { name: '角色管理', desc: '角色创建、编辑、删除、权限分配、状态管理' },
    { name: '菜单管理', desc: '菜单树形结构、类型分类、按钮级权限控制' },
    { name: '部门管理', desc: '部门层级结构、人员管理' },
    { name: '字典管理', desc: '字典类型与字典项管理、前端组件数据源' },
    { name: '系统配置', desc: '系统参数配置、配置热更新' },
    { name: '代码生成', desc: '基于模板的代码生成器、快速开发' },
    { name: '通知公告', desc: '系统通知发布、撤回、分级管理' }
];

yPosition = 1.5;
for (let i = 0; i < modules.length; i++) {
    const module = modules[i];
    const row = Math.floor(i / 2);
    const col = i % 2;

    slide.addText(module.name, {
        x: col === 0 ? 0.8 : 5.2,
        y: yPosition + row * 1.2,
        w: 3.5,
        h: 0.5,
        fontSize: 14,
        bold: true,
        color: 'FFFFFF',
        fill: { color: '97BC62' },
        align: 'center',
        valign: 'middle'
    });

    slide.addText(module.desc, {
        x: col === 0 ? 0.8 : 5.2,
        y: yPosition + row * 1.2 + 0.5,
        w: 3.5,
        h: 0.7,
        fontSize: 10,
        color: '333333',
        fill: { color: 'F2F2F2' },
        valign: 'top',
        margin: 0.1
    });
}

// 幻灯片6: 技术特色与优势
slide = pres.addSlide();
slide.addText('技术特色与优势', {
    x: 0.5,
    y: 0.3,
    w: 12.33,
    h: 0.8,
    fontSize: 32,
    bold: true,
    color: 'FFFFFF',
    fill: { color: '2C5F2D' },
    align: 'left'
});

const advantages = [
    { title: '现代化架构', desc: '采用最新的 Spring Boot 4、Java 17 等前沿技术栈' },
    { title: '安全性高', desc: 'JWT + Redis 双重认证，细粒度权限控制，安全可靠' },
    { title: '易于扩展', desc: '模块化设计，提供代码生成器，便于二次开发' },
    { title: '微服务友好', desc: '代码结构清晰，易于拆分为微服务架构' },
    { title: '前后端分离', desc: '支持主流前端框架（Vue 3、Element-Plus）' },
    { title: '功能完备', desc: '权限管理、日志记录、配置管理等功能齐全' }
];

yPosition = 1.5;
for (const advantage of advantages) {
    slide.addShape(pptx.ShapeType.rect, {
        x: 0.8,
        y: yPosition,
        w: 8.7,
        h: 0.8,
        fill: { color: 'F2F2F2' },
        line: { color: '97BC62', width: 2 }
    });

    slide.addText(advantage.title, {
        x: 1,
        y: yPosition,
        w: 2,
        h: 0.8,
        fontSize: 14,
        bold: true,
        color: 'FFFFFF',
        fill: { color: '97BC62' },
        align: 'center',
        valign: 'middle'
    });

    slide.addText(advantage.desc, {
        x: 3.2,
        y: yPosition,
        w: 6.3,
        h: 0.8,
        fontSize: 12,
        color: '333333',
        valign: 'middle',
        margin: 0.1
    });

    yPosition += 1;
}

// 幻灯片7: 开发特性
slide = pres.addSlide();
slide.addText('开发特性', {
    x: 0.5,
    y: 0.3,
    w: 12.33,
    h: 0.8,
    fontSize: 32,
    bold: true,
    color: 'FFFFFF',
    fill: { color: '2C5F2D' },
    align: 'left'
});

const devFeatures = [
    { feature: '接口文档', detail: '集成 Knife4j 实现接口文档自动生成' },
    { feature: '代码生成', detail: '提供基于模板的代码生成器，快速开发' },
    { feature: '统一异常处理', detail: '完善的全局异常处理机制' },
    { feature: '统一响应封装', detail: '标准化 API 响应格式' },
    { feature: '多环境配置', detail: '支持 dev、prod 等多种环境配置' },
    { feature: '日志记录', detail: '通过 @Log 注解实现操作日志记录' },
    { feature: 'AIGC集成', detail: '支持通义千问、DeepSeek 等AI模型' },
    { feature: '存储服务', detail: '集成MinIO、阿里云OSS等对象存储' }
];

yPosition = 1.5;
for (let i = 0; i < devFeatures.length; i++) {
    const item = devFeatures[i];
    const row = Math.floor(i / 2);
    const col = i % 2;

    slide.addText(item.feature, {
        x: col === 0 ? 0.8 : 5.2,
        y: yPosition + row * 1.0,
        w: 3.5,
        h: 0.4,
        fontSize: 14,
        bold: true,
        color: 'FFFFFF',
        fill: { color: '028090' },
        align: 'center',
        valign: 'middle'
    });

    slide.addText(item.detail, {
        x: col === 0 ? 0.8 : 5.2,
        y: yPosition + row * 1.0 + 0.4,
        w: 3.5,
        h: 0.6,
        fontSize: 10,
        color: '333333',
        fill: { color: 'F2F2F2' },
        valign: 'top',
        margin: 0.1
    });
}

// 幻灯片8: 总结
slide = pres.addSlide();
slide.addText('总结', {
    x: 0.5,
    y: 0.3,
    w: 12.33,
    h: 0.8,
    fontSize: 32,
    bold: true,
    color: 'FFFFFF',
    fill: { color: '2C5F2D' },
    align: 'left'
});

slide.addText('YouLai Boot 是一个功能完善、技术先进的权限管理系统，具备以下优势：', {
    x: 0.8,
    y: 1.5,
    fontSize: 16,
    bold: true,
    color: '2C5F2D'
});

const summaryPoints = [
    '1. 采用现代化技术栈，基于 Spring Boot 4 和 Java 17',
    '2. 安全性高，JWT + Redis 双重认证机制',
    '3. 权限控制精细，支持接口和按钮级别的权限控制',
    '4. 功能齐全，涵盖用户、角色、菜单、部门、字典等管理模块',
    '5. 易于扩展，提供代码生成器和模块化设计',
    '6. 适合用作企业级应用的基础框架'
];

yPosition = 2.2;
for (const point of summaryPoints) {
    slide.addText(point, {
        x: 0.8,
        y: yPosition,
        fontSize: 14,
        color: '333333',
        bullet: { code: '25A0' } // 使用方块作为项目符号
    });
    yPosition += 0.4;
}

slide.addText('适合用于快速搭建企业级应用的基础框架', {
    x: 0.8,
    y: 5.0,
    w: '85%',
    h: 0.8,
    fontSize: 18,
    bold: true,
    color: 'FFFFFF',
    fill: { color: '97BC62' },
    align: 'center',
    valign: 'middle'
});

// 保存PowerPoint文件
pres.writeFile('YouLai_Boot_技术架构介绍.pptx').then(() => {
    console.log('YouLai_Boot_技术架构介绍.pptx 文件已生成！');
}).catch(err => {
    console.error('生成PPT文件时出错:', err);

    // 如果直接生成失败，尝试另一种方式
    try {
        const fs = require('fs');
        const buffer = pres.generate({ outputType: 'nodebuffer' });
        fs.writeFileSync('YouLai_Boot_技术架构介绍.pptx', buffer);
        console.log('YouLai_Boot_技术架构介绍.pptx 文件已生成！');
    } catch (err2) {
        console.error('备选方案也失败了:', err2);
    }
});