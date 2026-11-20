export type OwnershipId = string | null | undefined;

function isValidOwnershipId(value: OwnershipId): value is string {
  return typeof value === 'string' && value.trim().length > 0;
}

export function canAccessOwnedResource(
  currentUserId: OwnershipId,
  resourceOwnerId: OwnershipId
): boolean {
  return (
    isValidOwnershipId(currentUserId) &&
    isValidOwnershipId(resourceOwnerId) &&
    currentUserId === resourceOwnerId
  );
}
