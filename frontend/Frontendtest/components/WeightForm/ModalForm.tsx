import { useDisclosure } from '@mantine/hooks';
import { Modal, Button, Group, Badge, MantineProvider } from '@mantine/core';
import { Calendar } from '@mantine/dates';

export default function ModalForm() {
  const [opened, { open, close }] = useDisclosure(false);

  return (
    <>
    <MantineProvider>
      <Modal opened={opened} onClose={close} title="Authentication">
        
        <Calendar />;
       
      </Modal>
      </MantineProvider>
      <Button variant="default" onClick={open}>
        Weight
      </Button>
    </>
  );
}