import { type MRT_TableInstance, type MRT_TableOptions } from './types';
export declare const useMantineReactTable: <TData extends Record<string, any> = {}>(tableOptions: MRT_TableOptions<TData>) => MRT_TableInstance<TData>;
