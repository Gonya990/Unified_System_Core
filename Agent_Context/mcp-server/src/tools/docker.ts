import Docker from 'dockerode';

// Connect to Docker via default socket (works on Linux host and inside properly configured containers)
const docker = new Docker({ socketPath: '/var/run/docker.sock' });

export async function listContainers() {
    try {
        const containers = await docker.listContainers({ all: true });
        return containers.map(c => ({
            id: c.Id.substring(0, 12),
            names: c.Names,
            image: c.Image,
            state: c.State,
            status: c.Status
        }));
    } catch (error: any) {
        console.error("Docker List Error:", error);
        throw new Error(`Failed to list containers: ${error.message}`);
    }
}

export async function restartContainer(id: string) {
    try {
        const container = docker.getContainer(id);
        await container.restart();
        return { status: 'success', message: `Container ${id} restarted` };
    } catch (error: any) {
        console.error(`Docker Restart Error (${id}):`, error);
        throw new Error(`Failed to restart container ${id}: ${error.message}`);
    }
}
