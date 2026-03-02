#!/usr/bin/env node
/**
 * Calendar MCP Server - Provides calendar operations via Google Calendar API
 * Tools: create_event, list_events, update_event, delete_event
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
  ? `${process.env.VAULT_PATH}/Logs/calendar_mcp_dev.log`
  : '/mnt/c/Users/Admin/AI_Employee_Vault/Logs/calendar_mcp_dev.log';
const EVENTS_FILE = process.env.VAULT_PATH
  ? `${process.env.VAULT_PATH}/Accounting/calendar_events.json`
  : '/mnt/c/Users/Admin/AI_Employee_Vault/Accounting/calendar_events.json';

// Simple logging
function log(message) {
  const timestamp = new Date().toISOString();
  const logLine = `[${timestamp}] ${message}\n`;
  console.error(logLine);
}

// Calendar OAuth setup
function getCalendarClient() {
  const clientId = process.env.GMAIL_CLIENT_ID;
  const clientSecret = process.env.GMAIL_CLIENT_SECRET;
  const refreshToken = process.env.GMAIL_REFRESH_TOKEN;

  if (!clientId || !clientSecret || !refreshToken) {
    return null;
  }

  const oauth2Client = new google.auth.OAuth2(clientId, clientSecret);
  oauth2Client.setCredentials({ refresh_token: refreshToken });

  return google.calendar({ version: 'v3', auth: oauth2Client });
}

// Load/save events (for DEV_MODE)
function loadEvents() {
  try {
    const fs = require('fs');
    if (fs.existsSync(EVENTS_FILE)) {
      return JSON.parse(fs.readFileSync(EVENTS_FILE, 'utf8'));
    }
  } catch (e) {}
  return [];
}

function saveEvents(events) {
  try {
    const fs = require('fs');
    const dir = require('path').dirname(EVENTS_FILE);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(EVENTS_FILE, JSON.stringify(events, null, 2));
  } catch (e) {
    log(`Failed to save events: ${e}`);
  }
}

// Tool definitions
const tools = [
  {
    name: 'create_event',
    description: 'Create a calendar event',
    inputSchema: {
      type: 'object',
      properties: {
        title: { type: 'string', description: 'Event title' },
        start: { type: 'string', description: 'Start time (ISO 8601)' },
        end: { type: 'string', description: 'End time (ISO 8601)' },
        attendees: { type: 'array', items: { type: 'string' }, description: 'Attendee emails' },
        description: { type: 'string', description: 'Event description' },
        location: { type: 'string', description: 'Event location' },
      },
      required: ['title', 'start', 'end'],
    },
  },
  {
    name: 'list_events',
    description: 'List calendar events in a date range',
    inputSchema: {
      type: 'object',
      properties: {
        date_range: { type: 'string', description: 'Date range (e.g., "2026-02-01 to 2026-02-28")' },
        max_results: { type: 'number', description: 'Maximum events to return', default: 10 },
      },
    },
  },
  {
    name: 'update_event',
    description: 'Update an existing calendar event',
    inputSchema: {
      type: 'object',
      properties: {
        id: { type: 'string', description: 'Event ID' },
        changes: { type: 'object', description: 'Fields to update' },
      },
      required: ['id', 'changes'],
    },
  },
  {
    name: 'delete_event',
    description: 'Delete a calendar event',
    inputSchema: {
      type: 'object',
      properties: {
        id: { type: 'string', description: 'Event ID' },
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

    // Store in DEV_MODE
    if (toolName === 'create_event') {
      const events = loadEvents();
      events.push({ ...args, id: `dev_${Date.now()}`, created_at: new Date().toISOString() });
      saveEvents(events);
    }

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({
            success: true,
            dev_mode: true,
            tool: toolName,
            args: args,
            message: 'DEV_MODE: Action logged',
          }),
        },
      ],
    };
  }

  const calendar = getCalendarClient();
  if (!calendar) {
    return {
      content: [{ type: 'text', text: JSON.stringify({ error: 'Google Calendar API not configured' }) }],
    };
  }

  try {
    let result;

    switch (toolName) {
      case 'create_event': {
        result = await calendar.events.insert({
          calendarId: 'primary',
          requestBody: {
            summary: args.title,
            description: args.description,
            location: args.location,
            start: { dateTime: args.start },
            end: { dateTime: args.end },
            attendees: (args.attendees || []).map(email => ({ email })),
          },
        });
        break;
      }

      case 'list_events': {
        const [start, end] = (args.date_range || '2026-02-01 to 2026-02-28').split(' to ');
        const response = await calendar.events.list({
          calendarId: 'primary',
          timeMin: new Date(start).toISOString(),
          timeMax: new Date(end).toISOString(),
          maxResults: args.max_results || 10,
          singleEvents: true,
          orderBy: 'startTime',
        });
        result = response.data.items || [];
        break;
      }

      case 'update_event': {
        result = await calendar.events.patch({
          calendarId: 'primary',
          eventId: args.id,
          requestBody: args.changes,
        });
        break;
      }

      case 'delete_event': {
        await calendar.events.delete({
          calendarId: 'primary',
          eventId: args.id,
        });
        result = { deleted: true };
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
  { name: 'calendar-mcp', version: '1.0.0' },
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

log('Calendar MCP Server started');
