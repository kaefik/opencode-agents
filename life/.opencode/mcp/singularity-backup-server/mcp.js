#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';
import { fileURLToPath } from 'url';

const execAsync = promisify(exec);
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const server = new Server(
  {
    name: 'singularity-backup-server',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'extract_singularity_data',
        description: 'Извлечь проекты и задачи из бэкапа Singularity. Поддерживает фильтрацию по статусу выполнения и статусу корзины.',
        inputSchema: {
          type: 'object',
          properties: {
            backup_file: {
              type: 'string',
              description: 'Путь к файлу бэкапа Singularity (по умолчанию: data/singularity_backup_2026-02-11.json)',
              default: 'data/singularity_backup_2026-02-11.json',
            },
            status: {
              type: 'string',
              enum: ['all', 'complete', 'incomplete'],
              description: 'Фильтр по статусу выполнения: all (все), complete (выполненные, checked=1), incomplete (не выполненные, checked=0)',
              default: 'all',
            },
            include_basket: {
              type: 'boolean',
              description: 'Включать задачи из корзины (true) или исключать (false)',
              default: true,
            },
            basket_only: {
              type: 'boolean',
              description: 'Только задачи из корзины (удаленные)',
              default: false,
            },
            json_output: {
              type: 'string',
              description: 'Путь к выходному JSON файлу',
              default: 'extracted_data.json',
            },
            md_output: {
              type: 'string',
              description: 'Путь к выходному Markdown файлу',
              default: 'extracted_data.md',
            },
          },
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === 'extract_singularity_data') {
    const {
      backup_file = 'data/singularity_backup_2026-02-11.json',
      status = 'all',
      include_basket = true,
      basket_only = false,
      json_output = 'extracted_data.json',
      md_output = 'extracted_data.md',
    } = args || {};

    try {
      const scriptPath = path.join(process.cwd(), 'scripts/extract_singularity_data.py');
      
      let cmd = `python3 "${scriptPath}"`;
      
      if (backup_file !== 'data/singularity_backup_2026-02-11.json') {
        cmd += ` "${backup_file}"`;
      }
      
      if (status !== 'all') {
        cmd += ` --status ${status}`;
      }
      
      if (include_basket === false && !basket_only) {
        cmd += ' --no-include-basket';
      }
      
      if (basket_only) {
        cmd += ' --basket-only';
      }
      
      if (json_output !== 'extracted_data.json') {
        cmd += ` --json-output "${json_output}"`;
      }
      
      if (md_output !== 'extracted_data.md') {
        cmd += ` --md-output "${md_output}"`;
      }

      const { stdout, stderr } = await execAsync(cmd);

      return {
        content: [
          {
            type: 'text',
            text: stdout || 'Данные успешно извлечены',
          },
        ],
      };
    } catch (error) {
      return {
        content: [
          {
            type: 'text',
            text: `Ошибка: ${error.message}\n${error.stderr || ''}`,
          },
        ],
        isError: true,
      };
    }
  }

  return {
    content: [
      {
        type: 'text',
        text: `Неизвестный инструмент: ${name}`,
      },
    ],
    isError: true,
  };
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
