import { Modal } from "@/components/Modal";
import { PopupSpec } from "@/components/admin/connectors/Popup";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { useState } from "react";
import { updateUserWhatsAppPhone } from "@/lib/user";
import { useUser } from "@/components/user/UserProvider";

interface Props {
  onClose: () => void;
  setPopup: (spec: PopupSpec) => void;
}

export function UserSettingsModal({ onClose, setPopup }: Props) {
  const { user, refreshUser } = useUser();
  const [phone, setPhone] = useState(user?.whatsapp_phone_number || "");
  const [loading, setLoading] = useState(false);

  const handleUpdatePhone = async () => {
    setLoading(true);
    try {
      const response = await updateUserWhatsAppPhone(phone || null);
      if (!response.ok) {
        const error = await response.json();
        setPopup({
          message: error.detail || "Failed to update WhatsApp phone number",
          type: "error",
        });
        return;
      }
      await refreshUser();
      setPopup({
        message: "WhatsApp phone number updated successfully",
        type: "success",
      });
    } catch (e) {
      console.error("Error updating WhatsApp phone number", e);
      setPopup({
        message: "Failed to update WhatsApp phone number",
        type: "error",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Modal title="User Settings" onOutsideClick={onClose}>
      <div className="flex flex-col gap-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            WhatsApp Phone Number
          </label>
          <p className="text-sm text-gray-500 mb-2">
            Enter your WhatsApp phone number with country code (e.g. +1234567890)
          </p>
          <Input
            type="tel"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            placeholder="+1234567890"
            pattern="^\+[1-9]\d{1,14}$"
            title="Please enter a valid phone number starting with + and country code"
          />
        </div>
        <Button onClick={handleUpdatePhone} disabled={loading}>
          {loading ? "Updating..." : "Update WhatsApp Phone"}
        </Button>
      </div>
    </Modal>
  );
}
