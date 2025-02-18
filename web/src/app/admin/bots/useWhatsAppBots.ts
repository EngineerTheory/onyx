import useSWR from "swr";

const fetcher = (url: string) => fetch(url).then((res) => res.json());

export function useWhatsAppBots() {
  const { data, error } = useSWR("/api/whatsapp/bots", fetcher);
  return {
    data,
    isLoading: !error && !data,
    error,
  };
}
