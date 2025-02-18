import React from "react";
import { Table } from "@/components/ui/table";
import Link from "next/link";

interface WhatsAppBot {
  id: number;
  name: string;
  enabled: boolean;
}

interface WhatsAppBotTableProps {
  whatsappBots: WhatsAppBot[];
}

export function WhatsAppBotTable({ whatsappBots }: WhatsAppBotTableProps) {
  return (
    <Table>
      <Table.Header>
        <Table.Row>
          <Table.Head>ID</Table.Head>
          <Table.Head>Name</Table.Head>
          <Table.Head>Status</Table.Head>
          <Table.Head>Actions</Table.Head>
        </Table.Row>
      </Table.Header>
      <Table.Body>
        {whatsappBots.map((bot) => (
          <Table.Row key={bot.id}>
            <Table.Cell>{bot.id}</Table.Cell>
            <Table.Cell>{bot.name}</Table.Cell>
            <Table.Cell>{bot.enabled ? "Enabled" : "Disabled"}</Table.Cell>
            <Table.Cell>
              <Link href={`/admin/bots/whatsapp/${bot.id}`}>Edit</Link>
            </Table.Cell>
          </Table.Row>
        ))}
      </Table.Body>
    </Table>
  );
}
