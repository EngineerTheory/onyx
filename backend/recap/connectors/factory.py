from typing import Any
from typing import Type

from sqlalchemy.orm import Session

from recap.configs.constants import DocumentSource
from recap.configs.constants import DocumentSourceRequiringTenantContext
from recap.connectors.airtable.airtable_connector import AirtableConnector
from recap.connectors.asana.connector import AsanaConnector
from recap.connectors.axero.connector import AxeroConnector
from recap.connectors.blob.connector import BlobStorageConnector
from recap.connectors.bookstack.connector import BookstackConnector
from recap.connectors.clickup.connector import ClickupConnector
from recap.connectors.confluence.connector import ConfluenceConnector
from recap.connectors.discord.connector import DiscordConnector
from recap.connectors.discourse.connector import DiscourseConnector
from recap.connectors.document360.connector import Document360Connector
from recap.connectors.dropbox.connector import DropboxConnector
from recap.connectors.egnyte.connector import EgnyteConnector
from recap.connectors.file.connector import LocalFileConnector
from recap.connectors.fireflies.connector import FirefliesConnector
from recap.connectors.freshdesk.connector import FreshdeskConnector
from recap.connectors.github.connector import GithubConnector
from recap.connectors.gitlab.connector import GitlabConnector
from recap.connectors.gmail.connector import GmailConnector
from recap.connectors.gong.connector import GongConnector
from recap.connectors.google_drive.connector import GoogleDriveConnector
from recap.connectors.google_site.connector import GoogleSitesConnector
from recap.connectors.guru.connector import GuruConnector
from recap.connectors.hubspot.connector import HubSpotConnector
from recap.connectors.interfaces import BaseConnector
from recap.connectors.interfaces import EventConnector
from recap.connectors.interfaces import LoadConnector
from recap.connectors.interfaces import PollConnector
from recap.connectors.linear.connector import LinearConnector
from recap.connectors.loopio.connector import LoopioConnector
from recap.connectors.mediawiki.wiki import MediaWikiConnector
from recap.connectors.models import InputType
from recap.connectors.notion.connector import NotionConnector
from recap.connectors.onyx_jira.connector import JiraConnector
from recap.connectors.productboard.connector import ProductboardConnector
from recap.connectors.salesforce.connector import SalesforceConnector
from recap.connectors.sharepoint.connector import SharepointConnector
from recap.connectors.slab.connector import SlabConnector
from recap.connectors.slack.connector import SlackPollConnector
from recap.connectors.teams.connector import TeamsConnector
from recap.connectors.web.connector import WebConnector
from recap.connectors.wikipedia.connector import WikipediaConnector
from recap.connectors.xenforo.connector import XenforoConnector
from recap.connectors.zendesk.connector import ZendeskConnector
from recap.connectors.zulip.connector import ZulipConnector
from recap.db.credentials import backend_update_credential_json
from recap.db.models import Credential


class ConnectorMissingException(Exception):
    pass


def identify_connector_class(
    source: DocumentSource,
    input_type: InputType | None = None,
) -> Type[BaseConnector]:
    connector_map = {
        DocumentSource.WEB: WebConnector,
        DocumentSource.FILE: LocalFileConnector,
        DocumentSource.SLACK: {
            InputType.POLL: SlackPollConnector,
            InputType.SLIM_RETRIEVAL: SlackPollConnector,
        },
        DocumentSource.GITHUB: GithubConnector,
        DocumentSource.GMAIL: GmailConnector,
        DocumentSource.GITLAB: GitlabConnector,
        DocumentSource.GOOGLE_DRIVE: GoogleDriveConnector,
        DocumentSource.BOOKSTACK: BookstackConnector,
        DocumentSource.CONFLUENCE: ConfluenceConnector,
        DocumentSource.JIRA: JiraConnector,
        DocumentSource.PRODUCTBOARD: ProductboardConnector,
        DocumentSource.SLAB: SlabConnector,
        DocumentSource.NOTION: NotionConnector,
        DocumentSource.ZULIP: ZulipConnector,
        DocumentSource.GURU: GuruConnector,
        DocumentSource.LINEAR: LinearConnector,
        DocumentSource.HUBSPOT: HubSpotConnector,
        DocumentSource.DOCUMENT360: Document360Connector,
        DocumentSource.GONG: GongConnector,
        DocumentSource.GOOGLE_SITES: GoogleSitesConnector,
        DocumentSource.ZENDESK: ZendeskConnector,
        DocumentSource.LOOPIO: LoopioConnector,
        DocumentSource.DROPBOX: DropboxConnector,
        DocumentSource.SHAREPOINT: SharepointConnector,
        DocumentSource.TEAMS: TeamsConnector,
        DocumentSource.SALESFORCE: SalesforceConnector,
        DocumentSource.DISCOURSE: DiscourseConnector,
        DocumentSource.AXERO: AxeroConnector,
        DocumentSource.CLICKUP: ClickupConnector,
        DocumentSource.MEDIAWIKI: MediaWikiConnector,
        DocumentSource.WIKIPEDIA: WikipediaConnector,
        DocumentSource.ASANA: AsanaConnector,
        DocumentSource.S3: BlobStorageConnector,
        DocumentSource.R2: BlobStorageConnector,
        DocumentSource.GOOGLE_CLOUD_STORAGE: BlobStorageConnector,
        DocumentSource.OCI_STORAGE: BlobStorageConnector,
        DocumentSource.XENFORO: XenforoConnector,
        DocumentSource.DISCORD: DiscordConnector,
        DocumentSource.FRESHDESK: FreshdeskConnector,
        DocumentSource.FIREFLIES: FirefliesConnector,
        DocumentSource.EGNYTE: EgnyteConnector,
        DocumentSource.AIRTABLE: AirtableConnector,
    }
    connector_by_source = connector_map.get(source, {})

    if isinstance(connector_by_source, dict):
        if input_type is None:
            # If not specified, default to most exhaustive update
            connector = connector_by_source.get(InputType.LOAD_STATE)
        else:
            connector = connector_by_source.get(input_type)
    else:
        connector = connector_by_source
    if connector is None:
        raise ConnectorMissingException(f"Connector not found for source={source}")

    if any(
        [
            input_type == InputType.LOAD_STATE
            and not issubclass(connector, LoadConnector),
            input_type == InputType.POLL and not issubclass(connector, PollConnector),
            input_type == InputType.EVENT and not issubclass(connector, EventConnector),
        ]
    ):
        raise ConnectorMissingException(
            f"Connector for source={source} does not accept input_type={input_type}"
        )
    return connector


def instantiate_connector(
    db_session: Session,
    source: DocumentSource,
    input_type: InputType,
    connector_specific_config: dict[str, Any],
    credential: Credential,
    tenant_id: str | None = None,
) -> BaseConnector:
    connector_class = identify_connector_class(source, input_type)

    if source in DocumentSourceRequiringTenantContext:
        connector_specific_config["tenant_id"] = tenant_id

    connector = connector_class(**connector_specific_config)
    new_credentials = connector.load_credentials(credential.credential_json)

    if new_credentials is not None:
        backend_update_credential_json(credential, new_credentials, db_session)

    return connector
