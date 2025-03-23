import { Accordion } from 'flowbite-react';

type Props = {
  summary: string;
  feedback: string;
};

export default function DiaryAccordion({ summary, feedback }: Props) {
  return (
    <div className="mt-20 mb-5 bg-white space-y-4">
      <Accordion>
        <Accordion.Panel>
          <Accordion.Title className="bg-gray-200 text-gray-800">この日は何をした日？</Accordion.Title>
          <Accordion.Content>
            <p className="mb-2 px-4 py-2 text-gray-500 dark:text-gray-400">{summary}</p>
          </Accordion.Content>
        </Accordion.Panel>
      </Accordion>
      <Accordion>
        <Accordion.Panel>
          <Accordion.Title className="bg-gray-200 text-gray-800">AIによる感想</Accordion.Title>
          <Accordion.Content>
            <p className="mb-2 px-4 py-2 text-gray-500 dark:text-gray-400">{feedback}</p>
          </Accordion.Content>
        </Accordion.Panel>
      </Accordion>
    </div>
  );
}
