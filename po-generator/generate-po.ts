import { Skill, Tool } from '@stevedorothy/claude-agent-sdk';

interface GeneratePOInput {
  tableName: string;
  className?: string;
  packageName?: string;
  author?: string;
}

// SQL字段类型到Java类型的映射
const TYPE_MAPPINGS: Record<string, string> = {
  'bigint': 'Long',
  'varchar': 'String',
  'char': 'String',
  'text': 'String',
  'mediumtext': 'String',
  'tinyint': 'Integer',
  'smallint': 'Integer',
  'int': 'Integer',
  'decimal': 'BigDecimal',
  'double': 'Double',
  'float': 'Float',
  'datetime': 'LocalDateTime',
  'timestamp': 'LocalDateTime',
  'date': 'LocalDate',
  'time': 'LocalTime',
  'json': 'String',
};

// 字段注释映射
const FIELD_COMMENTS: Record<string, string> = {
  'id': '主键ID',
  'create_time': '创建时间',
  'update_time': '更新时间',
  'create_by': '创建人 ID',
  'update_by': '更新人 ID',
  'is_deleted': '是否删除(0-否 1-是)',
  'parent_id': '父节点ID',
  'tree_path': '父节点ID路径',
  'sort': '排序',
  'status': '状态',
  'name': '名称',
  'code': '编码',
  'username': '用户名',
  'nickname': '昵称',
  'password': '密码',
  'email': '邮箱',
  'mobile': '手机',
  'avatar': '头像',
  'remark': '备注',
  'type': '类型',
  'content': '内容',
  'title': '标题',
  'ip': 'IP地址',
  'province': '省份',
  'city': '城市',
  'execution_time': '执行时间(ms)',
  'module': '日志模块',
  'request_method': '请求方式',
  'request_params': '请求参数',
  'response_content': '返回参数',
  'request_uri': '请求路径',
  'method': '方法名',
  'browser': '浏览器',
  'browser_version': '浏览器版本',
  'os': '终端系统',
  'config_name': '配置名称',
  'config_key': '配置键',
  'config_value': '配置值',
  'openid': '微信OpenID',
  'gender': '性别',
  'publish_status': '发布状态',
  'publish_time': '发布时间',
  'revoke_time': '撤回时间',
  'target_type': '目标类型',
  'target_user_ids': '目标用户ID集合',
  'publisher_id': '发布人ID',
  'level': '等级',
  'is_read': '读取状态',
  'read_time': '阅读时间',
  'ai_provider': 'AI供应商',
  'ai_model': 'AI模型名称',
  'parse_status': '解析是否成功',
  'function_calls': '解析出的函数调用列表',
  'explanation': 'AI的理解说明',
  'confidence': '置信度',
  'parse_error_message': '解析错误信息',
  'input_tokens': '输入Token数量',
  'output_tokens': '输出Token数量',
  'parse_duration_ms': '解析耗时(毫秒)',
  'function_name': '执行的函数名称',
  'function_arguments': '函数参数',
  'execute_status': '执行状态',
  'execute_error_message': '执行错误信息',
  'ip_address': 'IP地址',
  'dept_id': '部门ID',
};

/**
 * PO实体类生成器技能
 * 基于SQL表结构生成符合项目规范的PO实体类
 */
export const poGeneratorSkill: Skill = {
  name: 'po-generator',
  description: '基于数据库表结构生成符合项目规范的PO实体类',
  version: '1.0.0',
  parameters: {
    type: 'object',
    properties: {
      tableName: {
        type: 'string',
        description: '数据库表名',
      },
      className: {
        type: 'string',
        description: '实体类名（可选，默认根据表名推断）',
      },
      packageName: {
        type: 'string',
        description: '包名（可选，默认为 com.youlai.boot.system.model.entity）',
      },
      author: {
        type: 'string',
        description: '作者姓名（可选）',
      },
    },
    required: ['tableName'],
  },

  handler: async (input: GeneratePOInput) => {
    // 从SQL语句推断表结构（实际实现中这里应该从数据库或SQL文件获取）
    // 这里我们根据传入的表名模拟解析对应的表结构
    const tableInfo = await getTableStructure(input.tableName);

    if (!tableInfo) {
      return {
        error: `未找到表 ${input.tableName} 的结构定义`
      };
    }

    const className = input.className || toPascalCase(input.tableName.replace(/^sys_|^gen_/g, ''));
    const packageName = input.packageName || 'com.youlai.boot.system.model.entity';
    const author = input.author || 'Ray';

    let entityCode = `package ${packageName};\n\n`;

    entityCode += `import com.baomidou.mybatisplus.annotation.TableField;\n`;
    entityCode += `import com.baomidou.mybatisplus.annotation.TableName;\n`;
    entityCode += `import com.fasterxml.jackson.annotation.JsonInclude;\n`;
    entityCode += `import com.youlai.boot.common.base.BaseEntity;\n`;
    entityCode += `import lombok.Getter;\n`;
    entityCode += `import lombok.Setter;\n`;

    // 如果字段涉及日期类型，则导入相应包
    if (tableInfo.columns.some(col => ['datetime', 'timestamp', 'date', 'time'].includes(col.type))) {
      entityCode += `import java.time.LocalDateTime;\n`;
      entityCode += `import java.time.LocalDate;\n`;
      entityCode += `import java.time.LocalTime;\n`;
    }

    // 如果字段涉及数字类型，则导入相应包
    if (tableInfo.columns.some(col => ['decimal', 'double'].includes(col.type))) {
      entityCode += `import java.math.BigDecimal;\n`;
    }

    entityCode += `\n/**\n * ${tableInfo.comment || `${className}实体`}对象\n *\n`;
    if (author) {
      entityCode += ` * @author ${author}\n`;
    }
    entityCode += ` * @since ${new Date().toISOString().split('T')[0].replace(/-/g, '/')}\n`;
    entityCode += ` */\n`;
    entityCode += `@TableName("${tableInfo.name}")\n`;
    entityCode += `@Getter\n`;
    entityCode += `@Setter\n`;
    entityCode += `public class ${className} extends BaseEntity {\n\n`;

    // 生成字段
    for (const column of tableInfo.columns) {
      if (['id', 'create_time', 'update_time'].includes(column.name)) {
        continue; // 这些字段继承自BaseEntity
      }

      // 获取字段注释
      let fieldComment = column.comment;
      if (!fieldComment) {
        // 尝试从预定义注释映射中获取
        const mappedComment = FIELD_COMMENTS[column.name];
        if (mappedComment) {
          fieldComment = mappedComment;
        } else {
          // 默认使用字段名作为注释
          fieldComment = column.name;
        }
      }

      entityCode += `    /**\n`;
      entityCode += `     * ${fieldComment}\n`;
      entityCode += `     */\n`;

      // 如果不是默认映射类型，使用String类型
      const javaType = TYPE_MAPPINGS[column.type.split('(')[0]] || 'String';

      entityCode += `    private ${javaType} ${toCamelCase(column.name)};\n\n`;
    }

    entityCode += `}`;

    return {
      className,
      code: entityCode,
      message: `成功生成${className}实体类`
    };
  }
};

// 根据表名获取表结构（这里模拟实现，实际应从数据库或SQL文件获取）
async function getTableStructure(tableName: string) {
  // 这是从SQL文件中解析的实际表结构
  const tables: Record<string, any> = {
    'sys_user': {
      name: 'sys_user',
      comment: '系统用户表',
      columns: [
        { name: 'username', type: 'varchar', comment: '用户名' },
        { name: 'nickname', type: 'varchar', comment: '昵称' },
        { name: 'gender', type: 'tinyint', comment: '性别((1-男 2-女 0-保密)' },
        { name: 'password', type: 'varchar', comment: '密码' },
        { name: 'dept_id', type: 'int', comment: '部门ID' },
        { name: 'avatar', type: 'varchar', comment: '用户头像' },
        { name: 'mobile', type: 'varchar', comment: '联系方式' },
        { name: 'status', type: 'tinyint', comment: '状态(1-正常 0-禁用)' },
        { name: 'email', type: 'varchar', comment: '用户邮箱' },
        { name: 'create_by', type: 'bigint', comment: '创建人ID' },
        { name: 'update_by', type: 'bigint', comment: '修改人ID' },
        { name: 'is_deleted', type: 'tinyint', comment: '逻辑删除标识(0-未删除 1-已删除)' },
        { name: 'openid', type: 'char', comment: '微信 openid' }
      ]
    },
    'sys_dept': {
      name: 'sys_dept',
      comment: '部门管理表',
      columns: [
        { name: 'name', type: 'varchar', comment: '部门名称' },
        { name: 'code', type: 'varchar', comment: '部门编号' },
        { name: 'parent_id', type: 'bigint', comment: '父节点id' },
        { name: 'tree_path', type: 'varchar', comment: '父节点id路径' },
        { name: 'sort', type: 'smallint', comment: '显示顺序' },
        { name: 'status', type: 'tinyint', comment: '状态(1-正常 0-禁用)' },
        { name: 'create_by', type: 'bigint', comment: '创建人ID' },
        { name: 'update_by', type: 'bigint', comment: '修改人ID' },
        { name: 'is_deleted', type: 'tinyint', comment: '逻辑删除标识(1-已删除 0-未删除)' }
      ]
    },
    'sys_role': {
      name: 'sys_role',
      comment: '系统角色表',
      columns: [
        { name: 'name', type: 'varchar', comment: '角色名称' },
        { name: 'code', type: 'varchar', comment: '角色编码' },
        { name: 'sort', type: 'int', comment: '显示顺序' },
        { name: 'status', type: 'tinyint', comment: '角色状态(1-正常 0-停用)' },
        { name: 'data_scope', type: 'tinyint', comment: '数据权限(1-所有数据 2-部门及子部门数据 3-本部门数据 4-本人数据)' },
        { name: 'create_by', type: 'bigint', comment: '创建人 ID' },
        { name: 'update_by', type: 'bigint', comment: '更新人ID' },
        { name: 'is_deleted', type: 'tinyint', comment: '逻辑删除标识(0-未删除 1-已删除)' }
      ]
    },
    'sys_menu': {
      name: 'sys_menu',
      comment: '系统菜单表',
      columns: [
        { name: 'parent_id', type: 'bigint', comment: '父菜单ID' },
        { name: 'tree_path', type: 'varchar', comment: '父节点ID路径' },
        { name: 'name', type: 'varchar', comment: '菜单名称' },
        { name: 'type', type: 'char', comment: '菜单类型（C-目录 M-菜单 B-按钮）' },
        { name: 'route_name', type: 'varchar', comment: '路由名称（Vue Router 中用于命名路由）' },
        { name: 'route_path', type: 'varchar', comment: '路由路径（Vue Router 中定义的 URL 路径）' },
        { name: 'component', type: 'varchar', comment: '组件路径（组件页面完整路径，相对于 src/views/，缺省后缀 .vue）' },
        { name: 'perm', type: 'varchar', comment: '【按钮】权限标识' },
        { name: 'always_show', type: 'tinyint', comment: '【目录】只有一个子路由是否始终显示（1-是 0-否）' },
        { name: 'keep_alive', type: 'tinyint', comment: '【菜单】是否开启页面缓存（1-是 0-否）' },
        { name: 'visible', type: 'tinyint', comment: '显示状态（1-显示 0-隐藏）' },
        { name: 'sort', type: 'int', comment: '排序' },
        { name: 'icon', type: 'varchar', comment: '菜单图标' },
        { name: 'redirect', type: 'varchar', comment: '跳转路径' },
        { name: 'create_by', type: 'bigint', comment: '创建人ID' },
        { name: 'update_by', type: 'bigint', comment: '更新人ID' },
        { name: 'params', type: 'varchar', comment: '路由参数' }
      ]
    },
    'sys_dict': {
      name: 'sys_dict',
      comment: '数据字典类型表',
      columns: [
        { name: 'dict_code', type: 'varchar', comment: '类型编码' },
        { name: 'name', type: 'varchar', comment: '类型名称' },
        { name: 'status', type: 'tinyint', comment: '状态(0:正常;1:禁用)' },
        { name: 'remark', type: 'varchar', comment: '备注' },
        { name: 'create_time', type: 'datetime', comment: '创建时间' },
        { name: 'create_by', type: 'bigint', comment: '创建人ID' },
        { name: 'update_time', type: 'datetime', comment: '更新时间' },
        { name: 'update_by', type: 'bigint', comment: '修改人ID' },
        { name: 'is_deleted', type: 'tinyint', comment: '是否删除(1-删除，0-未删除)' }
      ]
    },
    'sys_dict_item': {
      name: 'sys_dict_item',
      comment: '数据字典项表',
      columns: [
        { name: 'dict_code', type: 'varchar', comment: '关联字典编码，与sys_dict表中的dict_code对应' },
        { name: 'value', type: 'varchar', comment: '字典项值' },
        { name: 'label', type: 'varchar', comment: '字典项标签' },
        { name: 'tag_type', type: 'varchar', comment: '标签类型，用于前端样式展示（如success、warning等）' },
        { name: 'status', type: 'tinyint', comment: '状态（1-正常，0-禁用）' },
        { name: 'sort', type: 'int', comment: '排序' },
        { name: 'remark', type: 'varchar', comment: '备注' },
        { name: 'create_time', type: 'datetime', comment: '创建时间' },
        { name: 'create_by', type: 'bigint', comment: '创建人ID' },
        { name: 'update_time', type: 'datetime', comment: '更新时间' },
        { name: 'update_by', type: 'bigint', comment: '修改人ID' }
      ]
    },
    'sys_log': {
      name: 'sys_log',
      comment: '系统操作日志表',
      columns: [
        { name: 'module', type: 'varchar', comment: '日志模块' },
        { name: 'request_method', type: 'varchar', comment: '请求方式' },
        { name: 'request_params', type: 'text', comment: '请求参数(批量请求参数可能会超过text)' },
        { name: 'response_content', type: 'mediumtext', comment: '返回参数' },
        { name: 'content', type: 'varchar', comment: '日志内容' },
        { name: 'request_uri', type: 'varchar', comment: '请求路径' },
        { name: 'method', type: 'varchar', comment: '方法名' },
        { name: 'ip', type: 'varchar', comment: 'IP地址' },
        { name: 'province', type: 'varchar', comment: '省份' },
        { name: 'city', type: 'varchar', comment: '城市' },
        { name: 'execution_time', type: 'bigint', comment: '执行时间(ms)' },
        { name: 'browser', type: 'varchar', comment: '浏览器' },
        { name: 'browser_version', type: 'varchar', comment: '浏览器版本' },
        { name: 'os', type: 'varchar', comment: '终端系统' },
        { name: 'create_by', type: 'bigint', comment: '创建人ID' }
      ]
    },
    'sys_config': {
      name: 'sys_config',
      comment: '系统配置表',
      columns: [
        { name: 'config_name', type: 'varchar', comment: '配置名称' },
        { name: 'config_key', type: 'varchar', comment: '配置key' },
        { name: 'config_value', type: 'varchar', comment: '配置值' },
        { name: 'remark', type: 'varchar', comment: '备注' },
        { name: 'create_by', type: 'bigint', comment: '创建人ID' },
        { name: 'update_by', type: 'bigint', comment: '更新人ID' },
        { name: 'is_deleted', type: 'tinyint', comment: '逻辑删除标识(0-未删除 1-已删除)' }
      ]
    },
    'sys_notice': {
      name: 'sys_notice',
      comment: '系统通知公告表',
      columns: [
        { name: 'title', type: 'varchar', comment: '通知标题' },
        { name: 'content', type: 'text', comment: '通知内容' },
        { name: 'type', type: 'tinyint', comment: '通知类型（关联字典编码：notice_type）' },
        { name: 'level', type: 'varchar', comment: '通知等级（字典code：notice_level）' },
        { name: 'target_type', type: 'tinyint', comment: '目标类型（1: 全体, 2: 指定）' },
        { name: 'target_user_ids', type: 'varchar', comment: '目标人ID集合（多个使用英文逗号,分割）' },
        { name: 'publisher_id', type: 'bigint', comment: '发布人ID' },
        { name: 'publish_status', type: 'tinyint', comment: '发布状态（0: 未发布, 1: 已发布, -1: 已撤回）' },
        { name: 'publish_time', type: 'datetime', comment: '发布时间' },
        { name: 'revoke_time', type: 'datetime', comment: '撤回时间' },
        { name: 'create_by', type: 'bigint', comment: '创建人ID' },
        { name: 'update_by', type: 'bigint', comment: '更新人ID' },
        { name: 'is_deleted', type: 'tinyint', comment: '是否删除（0: 未删除, 1: 已删除）' }
      ]
    },
    'sys_user_notice': {
      name: 'sys_user_notice',
      comment: '用户通知公告关联表',
      columns: [
        { name: 'notice_id', type: 'bigint', comment: '公共通知id' },
        { name: 'user_id', type: 'bigint', comment: '用户id' },
        { name: 'is_read', type: 'bigint', comment: '读取状态（0: 未读, 1: 已读）' },
        { name: 'read_time', type: 'datetime', comment: '阅读时间' },
        { name: 'create_time', type: 'datetime', comment: '创建时间' },
        { name: 'update_time', type: 'datetime', comment: '更新时间' },
        { name: 'is_deleted', type: 'tinyint', comment: '逻辑删除(0: 未删除, 1: 已删除)' }
      ]
    },
    'ai_assistant_record': {
      name: 'ai_assistant_record',
      comment: 'AI 助手行为记录表（解析、执行、审计）',
      columns: [
        { name: 'user_id', type: 'bigint', comment: '用户ID' },
        { name: 'username', type: 'varchar', comment: '用户名' },
        { name: 'original_command', type: 'text', comment: '原始命令' },
        { name: 'ai_provider', type: 'varchar', comment: 'AI 供应商(qwen/openai/deepseek/gemini等)' },
        { name: 'ai_model', type: 'varchar', comment: 'AI 模型名称(qwen-plus/qwen-max/gpt-4-turbo等)' },
        { name: 'parse_status', type: 'tinyint', comment: '解析是否成功(0-失败, 1-成功)' },
        { name: 'function_calls', type: 'text', comment: '解析出的函数调用列表(JSON)' },
        { name: 'explanation', type: 'varchar', comment: 'AI的理解说明' },
        { name: 'confidence', type: 'decimal', comment: '置信度(0.00-1.00)' },
        { name: 'parse_error_message', type: 'text', comment: '解析错误信息' },
        { name: 'input_tokens', type: 'int', comment: '输入Token数量' },
        { name: 'output_tokens', type: 'int', comment: '输出Token数量' },
        { name: 'parse_duration_ms', type: 'int', comment: '解析耗时(毫秒)' },
        { name: 'function_name', type: 'varchar', comment: '执行的函数名称' },
        { name: 'function_arguments', type: 'text', comment: '函数参数(JSON)' },
        { name: 'execute_status', type: 'tinyint', comment: '执行状态(0-待执行, 1-成功, -1-失败)' },
        { name: 'execute_error_message', type: 'text', comment: '执行错误信息' },
        { name: 'ip_address', type: 'varchar', comment: 'IP地址' }
      ]
    },
    'gen_table': {
      name: 'gen_table',
      comment: '代码生成配置表',
      columns: [
        { name: 'table_name', type: 'varchar', comment: '表名' },
        { name: 'module_name', type: 'varchar', comment: '模块名' },
        { name: 'package_name', type: 'varchar', comment: '包名' },
        { name: 'business_name', type: 'varchar', comment: '业务名' },
        { name: 'entity_name', type: 'varchar', comment: '实体类名' },
        { name: 'author', type: 'varchar', comment: '作者' },
        { name: 'parent_menu_id', type: 'bigint', comment: '上级菜单ID，对应sys_menu的id ' },
        { name: 'remove_table_prefix', type: 'varchar', comment: '要移除的表前缀，如: sys_' },
        { name: 'page_type', type: 'varchar', comment: '页面类型(classic|curd)' }
      ]
    },
    'gen_table_column': {
      name: 'gen_table_column',
      comment: '代码生成字段配置表',
      columns: [
        { name: 'table_id', type: 'bigint', comment: '关联的表配置ID' },
        { name: 'column_name', type: 'varchar', comment: '' },
        { name: 'column_type', type: 'varchar', comment: '' },
        { name: 'column_length', type: 'int', comment: '' },
        { name: 'field_name', type: 'varchar', comment: '字段名称' },
        { name: 'field_type', type: 'varchar', comment: '字段类型' },
        { name: 'field_sort', type: 'int', comment: '字段排序' },
        { name: 'field_comment', type: 'varchar', comment: '字段描述' },
        { name: 'max_length', type: 'int', comment: '' },
        { name: 'is_required', type: 'tinyint', comment: '是否必填' },
        { name: 'is_show_in_list', type: 'tinyint', comment: '是否在列表显示' },
        { name: 'is_show_in_form', type: 'tinyint', comment: '是否在表单显示' },
        { name: 'is_show_in_query', type: 'tinyint', comment: '是否在查询条件显示' },
        { name: 'query_type', type: 'tinyint', comment: '查询方式' },
        { name: 'form_type', type: 'tinyint', comment: '表单类型' },
        { name: 'dict_type', type: 'varchar', comment: '字典类型' }
      ]
    }
  };

  return tables[tableName];
}

// 将字符串转换为驼峰命名
function toCamelCase(str: string): string {
  return str.replace(/_([a-z])/g, (match, letter) => letter.toUpperCase());
}

// 将字符串转换为帕斯卡命名（首字母大写）
function toPascalCase(str: string): string {
  const camelCase = toCamelCase(str);
  return camelCase.charAt(0).toUpperCase() + camelCase.slice(1);
}