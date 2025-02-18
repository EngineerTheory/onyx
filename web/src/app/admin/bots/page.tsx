"use client";

import { ErrorCallout } from "@/components/ErrorCallout";
import { ThreeDotsLoader } from "@/components/Loading";
import { InstantSSRAutoRefresh } from "@/components/SSRAutoRefresh";
import { AdminPageTitle } from "@/components/admin/Title";
import { SourceIcon } from "@/components/SourceIcon";
import { SlackBotTable } from "./SlackBotTable";
import { useSlackBots } from "./[bot-id]/hooks";
import { ValidSources } from "@/lib/types";
import CreateButton from "@/components/ui/createButton";

import { WhatsAppBotTable } from "./WhatsAppBotTable";
import { useWhatsAppBots } from "./useWhatsAppBots";

const Main = () => {
  const {
    data: slackBots,
    isLoading: isSlackBotsLoading,
    error: slackBotsError,
  } = useSlackBots();

  const {
    data: whatsappBots,
    isLoading: isWhatsappBotsLoading,
    error: whatsappBotsError,
  } = useWhatsAppBots();

  return (
    <div className="mb-8">
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Slack Integration</h2>
        <p className="mb-2 text-sm text-muted-foreground">
          Setup Slack bots that connect to Onyx. Once setup, you will be able to ask
          questions to Onyx directly from Slack. Additionally, you can:
        </p>
        <div className="mb-2">
          <ul className="list-disc mt-2 ml-4 text-sm text-muted-foreground">
            <li>
              Have OnyxBot automatically answer questions in designated channels.
            </li>
            <li>
              Choose document sets OnyxBot should answer from based on the channel.
            </li>
            <li>
              Directly message OnyxBot to search similar to the web UI.
            </li>
          </ul>
        </div>
        <p className="mb-6 text-sm text-muted-foreground">
          For setup instructions, refer to the documentation guide.
        </p>
        <CreateButton href="/admin/bots/new" text="New Slack Bot" />
        {isSlackBotsLoading ? (
          <div>Loading Slack bots...</div>
        ) : slackBotsError ? (
          <div>Error loading Slack bots</div>
        ) : (
          <SlackBotTable slackBots={slackBots} />
        )}
      </div>

      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">WhatsApp Integration</h2>
        <p className="mb-2 text-sm text-muted-foreground">
          Configure the WhatsApp bot by activating it below the Slack integration.
          Users can connect their accounts using their phone number.
        </p>
        <CreateButton href="/admin/bots/whatsapp/new" text="New WhatsApp Bot" />
        {isWhatsappBotsLoading ? (
          <div>Loading WhatsApp bots...</div>
        ) : whatsappBotsError ? (
          <div>Error loading WhatsApp bots</div>
        ) : (
          <WhatsAppBotTable whatsappBots={whatsappBots} />
        )}
      </div>
    </div>
  );
};

const Page = () => {
  return (
    <div className="container mx-auto">
      <AdminPageTitle
        icon={<SourceIcon iconSize={36} sourceType={ValidSources.Slack} />}
        title="Bot Integrations"
      />
      <InstantSSRAutoRefresh />
      <Main />
    </div>
  );
};

export default Page;
