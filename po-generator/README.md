# PO实体类生成技能使用指南

## 概述
PO（Persistent Object）实体类生成技能是一个用于快速生成符合项目规范的Java实体类的工具。它可以根据数据库表结构自动生成带有适当注解和注释的实体类。

## 功能特点
- 基于数据库表结构自动生成Java实体类
- 遵循项目代码规范和架构模式
- 支持MyBatis-Plus注解（@TableName、@TableField）
- 自动映射SQL字段类型到Java类型
- 自动生成类和字段注释
- 继承BaseEntity基类，使用Lombok注解
- 支持Jackson注解用于JSON序列化控制

## SQL类型到Java类型的映射
- `bigint` → `Long`
- `varchar`, `char`, `text`, `mediumtext`, `json` → `String`
- `tinyint`, `smallint`, `int` → `Integer`
- `decimal` → `BigDecimal`
- `double`, `float` → `Double`, `Float`
- `datetime`, `timestamp` → `LocalDateTime`
- `date` → `LocalDate`
- `time` → `LocalTime`

## 生成的实体类特征
1. **包声明**：默认使用`com.youlai.boot.system.model.entity`包
2. **继承关系**：继承`BaseEntity`基类
3. **注解使用**：
   - `@TableName`：指定数据库表名
   - `@Getter`和`@Setter`：Lombok注解，生成getter/setter方法
4. **字段处理**：
   - 跳过已在BaseEntity中定义的字段（id, create_time, update_time）
   - 根据SQL字段类型自动映射Java类型
   - 为每个字段生成合适的注释
5. **导入必要的包**：根据使用的类型自动导入相关包

## 示例输出
生成的实体类如下所示：
```java
package com.youlai.boot.system.model.entity;

import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.youlai.boot.common.base.BaseEntity;
import lombok.Getter;
import lombok.Setter;

/**
 * 部门实体对象
 *
 * @author Claude
 * @since 2026/03/19
 */
@TableName("sys_dept")
@Getter
@Setter
public class Dept extends BaseEntity {

    /**
     * 部门名称
     */
    private String name;

    /**
     * 部门编号
     */
    private String code;

    /**
     * 父节点id
     */
    private Long parentId;

    /**
     * 父节点id路径
     */
    private String treePath;

    /**
     * 显示顺序
     */
    private Integer sort;

    /**
     * 状态(1-正常 0-禁用)
     */
    private Integer status;

    /**
     * 创建人 ID
     */
    private Long createBy;

    /**
     * 更新人 ID
     */
    private Long updateBy;

    /**
     * 是否删除(0-否 1-是)
     */
    private Integer isDeleted;

}
```

## 支持的表
技能支持以下系统表的实体类生成：
- sys_user (用户表)
- sys_dept (部门表)
- sys_role (角色表)
- sys_menu (菜单表)
- sys_dict (字典表)
- sys_dict_item (字典项表)
- sys_log (日志表)
- sys_config (配置表)
- sys_notice (通知公告表)
- sys_user_notice (用户通知关联表)
- ai_assistant_record (AI助手记录表)
- gen_table (代码生成配置表)
- gen_table_column (代码生成字段配置表)

## 使用方法
1. 确保你的项目结构与YouLai Boot项目兼容
2. 调用技能并提供相应的参数
3. 根据需要调整生成的实体类代码
4. 将生成的实体类保存到正确的包路径下

## 注意事项
- 生成的实体类基于SQL文件中的表结构定义
- 如果需要自定义包名或作者，可以通过参数指定
- 生成的类遵循项目现有的命名约定和注释风格
- 基本上支持所有的基础数据类型，复杂类型需要手工调整