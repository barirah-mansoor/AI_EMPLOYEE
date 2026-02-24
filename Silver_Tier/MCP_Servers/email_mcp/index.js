#!/usr/bin/env node
/**
 * Email MCP Server - Provides email operations via Gmail API
 * Tools: send_email, draft_email, search_emails, get_email
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { google } from 'googleapis';

// Configuration
const DEV_MODE = process.env.DEV_MODE === 'true';
const LOG_FILE = process.env.VAULT_PATH
  ? `${process.env.VAULT_PATH}/Logs/email_mcp_dev.log`
  : '/mnt/c/Users/Admin/AI_Employee_Vault/Logs/email_mcp_dev.log';

// Simple logging
function log(message) {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] ${message}\n`;
  try {
    const fs = await import('fs');
    fs.appendFileSync(LOG_FILE, logLine);
  } catch (e) {
    console.error('Log write failed:', e);
  }
  console.error(message);
}

// Gmail OAuth setup
function getGmailClient() {
  const clientId = process.env.GMAIL_CLIENT_ID;
  const clientSecret = process.env.GMAIL_CLIENT_SECRET;
  const refreshToken = process.env.GMAIL_REFRESH_TOKEN;

  if (!clientId || !clientSecret || !refreshToken) {
    return null;
  }

  const oauth2Client = new google.auth.OAuth2(clientId, clientSecret);
  oauth2Client.setCredentials({ refresh_token: refreshToken });

  return google.gmail({ version: 'v1', auth: oauth2Client });
}

// Tool definitions
const tools = [
  {
    name: 'send_email',
    description: 'Send an email via Gmail API',
    inputSchema: {
      type: 'object',
      properties: {
        to: { type: 'string', description: 'Recipient email address' },
        subject: { type: 'string', description: 'Email subject' },
        body: { type: 'string', description: 'Email body content' },
        attachment: { type: 'string', description: 'Optional file path to attach' },
      },
      required: ['to', 'subject', 'body'],
    },
  },
  {
    name: 'draft_email',
    description: 'Create a draft email in Gmail',
    inputSchema: {
      type: 'object',
      properties: {
        to: { type: 'string', description: 'Recipient email address' },
        subject: { type: 'string', description: 'Email subject' },
        body: { type: 'string', description: 'Email body content' },
      },
      required: ['to', 'subject', 'body'],
    },
  },
  {
    name: 'search_emails',
    description: 'Search emails in Gmail',
    inputSchema: {
      type: 'object',
      properties: {
        query: { type: 'string', description: 'Gmail search query' },
        maxResults: { type: 'number', description: 'Maximum results to return', default: 10 },
      },
      required: ['query'],
    },
  },
  {
    name: 'get_email',
    description: 'Get a specific email by ID',
    inputSchema: {
      type: 'object',
      properties: {
        id: { type: 'string', description: 'Email ID' },
      },
      required: ['id'],
    },
  },
];

// Tool handlers
async function handleToolCall(toolName, args) {
  log(`Tool call: ${toolName}`);

  if (DEV_MODE) {
    log(`DEV_MODE: Would execute ${toolName} with args: ${JSON.stringify(args)}`);
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            dev_mode: true,
            tool: toolName,
            args: args,
            message: 'DEV_MODE: Action logged, not executed',
          }),
        },
      ],
    };
  }

  const gmail = getGmailClient();
  if (!gmail) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({ error: 'Gmail API not configured' }),
        },
      ],
    };
  }

  try {
    let result;

    switch (toolName) {
      case 'send_email': {
        const message = [
          `To: ${args.to}`,
          'Content-Type: text/html; charset=utf-8',
          `Subject: ${args.subject}`,
          '',
          args.body,
        ].join('\n');

        const encodedMessage = Buffer.from(message).toString('base64url');
        result = await gmail.users.messages.send({
          userId: 'me',
          requestBody: { raw: encodedMessage },
        });
        break;
      }

      case 'draft_email': {
        const message = [
          `To: ${args.to}`,
          'Content-Type: text/html; charset=utf-8',
          `Subject: ${args.subject}`,
          '',
          args.body,
        ].join('\n');

        const encodedMessage = Buffer.from(message).toString('base64url');
        result = await gmail.users.drafts.create({
          userId: 'me',
          requestBody: {
            message: { raw: encodedMessage },
          },
        });
        break;
      }

      case 'search_emails': {
        const response = await gmail.users.messages.list({
          userId: 'me',
          q: args.query,
          maxResults: args.maxResults || 10,
        });
        result = response.data.messages || [];
        break;
      }

      case 'get_email': {
        result = await gmail.users.messages.get({
          userId: 'me',
          id: args.id,
          format: 'full',
        });
        break;
      }

      default:
        return { content: [{ type: 'text', text: JSON.stringify({ error: 'Unknown tool' }) }] };
    }

    return {
      content: [{ type: 'text', text: JSON.stringify({ success: true, data: result }) }],
    };
  } catch (error) {
    log(`Error: ${error.message}`);
    return {
      content: [{ type: 'text', text: JSON.stringify({ error: error.message }) }],
    };
  }
}

// Server setup
const server = new Server(
  { name: 'email-mcp', version: '1.0.0' },
  {
    capabilities: { tools: {} },
  }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools,
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  return handleToolCall(name, args);
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);

log('Email MCP Server started');
